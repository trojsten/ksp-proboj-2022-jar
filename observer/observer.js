function setupCanvas(canvas) {
    let rect = canvas.getBoundingClientRect()
    canvas.width = rect.width
    canvas.height = rect.height
    let ctx = canvas.getContext('2d')
    return ctx
}

const CANVAS = document.querySelector('.canvas')
const CTX = setupCanvas(CANVAS)
let GRID = 0
let OBSLINES = []
let FRAME = 0
const urlParams = new URLSearchParams(window.location.search)

async function showFile(f) {
    let file = f.files[0]
    let data = await file.arrayBuffer()
    observe(data)
}

function observe(log) {
    log = new Uint8Array(log)
    try {
        log = pako.inflate(log)
        log = new TextDecoder().decode(log)
    } catch (err) {
        alert("error while inflating: " + err)
        return
    }

    lines = log.split("\n")
    OBSLINES = []
    for (let i = 0; i < lines.length; i++) {
        if (!lines[i]) {
            continue
        }
        OBSLINES.push(JSON.parse(lines[i]))
    }

    FRAME = 0
    renderFrame(0)

    if (urlParams.get("autoplay") === "1") {
        PLAYBACK.playing = true
    }
}

const ARROWS = {
    "U": [[1/2, 1/4], [3/4, 3/4], [1/4, 3/4]], // 0 -1
    "D": [[1/2, 3/4], [3/4, 1/4], [1/4, 1/4]], // 0 1
    "L": [[1/4, 1/2], [3/4, 1/4], [3/4, 3/4]], // -1 0
    "R": [[3/4, 1/2], [1/4, 1/4], [1/4, 3/4]], // 1 0
}

const POWERUP_COLORS = ["yellow", "gold"]

function renderPlayers(f) {
    document.getElementById("players").innerHTML = ''
    const frame = OBSLINES[f]
    for (const player of frame.Players) {
        document.getElementById("players").innerHTML += `
            <div class="player ${player.Alive ? '' : 'player-dead'}">
                <div class="player-color" style="background: ${player.Color}"></div>
                <div class="player-name">${player.DisplayName}</div>
                <div class="player-score">${frame.Scores[player.Name]}</div>
            </div>`
    }
}

function renderFrame(f) {
    const frame = OBSLINES[f]
    GRID = Math.min(CANVAS.width / frame.Map.Width, CANVAS.height / frame.Map.Height)
    CTX.clearRect(0, 0, CANVAS.width, CANVAS.height);

    CTX.shadowColor = null
    CTX.shadowBlur = null
    CTX.strokeStyle = 'rgba(26,26,26)'
    for (let x = 0; x < frame.Map.Width; x++) { 
        CTX.beginPath()
        CTX.moveTo(x * GRID, 0)
        CTX.lineTo(x * GRID, frame.Map.Height * GRID)
        CTX.stroke()
    }
    for (let y = 0; y < frame.Map.Height; y++) { 
        CTX.beginPath()
        CTX.moveTo(0, y * GRID)
        CTX.lineTo(frame.Map.Width * GRID, y * GRID)
        CTX.stroke()
    }
    CTX.strokeStyle = null

    for (let x = 0; x < frame.Map.Width; x++) {
        for (let y = 0; y < frame.Map.Height; y++) {
            const tile = frame.Map.Contents[x][y]
            if (tile === -1) {
                continue
            }
            CTX.beginPath()
            if (tile >= 0) {
                CTX.fillStyle = frame.Players[tile].Alive ? frame.Players[tile].Color : "#555"
            } else {
                CTX.fillStyle = "#fff"
            }
            CTX.shadowColor = CTX.fillStyle
            CTX.shadowBlur = GRID/4
            CTX.rect(x * GRID, y * GRID, GRID, GRID)
            CTX.fill()
        }
    }
    CTX.shadowColor = null

    for (const player of frame.Players) {
        if (!player.Alive) {
            continue
        }

        CTX.beginPath()
        CTX.fillStyle = "rgba(255,255,255,0.75)"

        ox = GRID * player.X
        oy = GRID * player.Y
        arrow = ARROWS["U"]
        if (player.Dx === 0 && player.Dy === 1) {
            arrow = ARROWS["D"]
        } else if (player.Dx === -1 && player.Dy === 0) {
            arrow = ARROWS["L"]
        } else if (player.Dx === 1 && player.Dy === 0) {
            arrow = ARROWS["R"]
        }

        CTX.moveTo(ox + GRID * arrow[0][0], oy + GRID * arrow[0][1])
        CTX.lineTo(ox + GRID * arrow[1][0], oy + GRID * arrow[1][1])
        CTX.lineTo(ox + GRID * arrow[2][0], oy + GRID * arrow[2][1])
        CTX.fill()
    }

    for (const up of frame.PowerUps) {
        CTX.beginPath()
        CTX.fillStyle = POWERUP_COLORS[f % POWERUP_COLORS.length]
        CTX.shadowColor = CTX.fillStyle
        CTX.shadowBlur = GRID/4
        CTX.arc(up.X * GRID + GRID/2, up.Y * GRID + GRID/2, GRID/2, 0, 2*Math.PI)
        CTX.fill()
        CTX.shadowColor = null
    }

    renderPlayers(f)
}

let PLAYBACK = {
    playing: false,
    speed: 200
}

document.getElementById("js-frame-prev").addEventListener("click", () => {
    FRAME--
    FRAME = Math.max(FRAME, 0)
    renderFrame(FRAME)
})

document.getElementById("js-frame-next").addEventListener("click", () => {
    FRAME++
    FRAME = Math.min(FRAME, OBSLINES.length - 1)
    renderFrame(FRAME)
})

document.getElementById("js-speed-slower").addEventListener("click", () => {
    PLAYBACK.speed += 20
})

document.getElementById("js-speed-faster").addEventListener("click", () => {
    PLAYBACK.speed -= 20
    PLAYBACK.speed = Math.max(PLAYBACK.speed, 20)
})

document.getElementById("js-play").addEventListener("click", () => {
    PLAYBACK.playing = true
})

document.getElementById("js-pause").addEventListener("click", () => {
    PLAYBACK.playing = false
})

function playTick() {
    if (PLAYBACK.playing) {
        if (FRAME < OBSLINES.length - 1) {
            FRAME++
            renderFrame(FRAME)
        } else {
            PLAYBACK.playing = false

            if (urlParams.get("autoplay") === "1") {
                setTimeout(() => {window.location = "/autoplay/"}, 2500)
            }
        }
    }
    setTimeout(playTick, PLAYBACK.speed)
}

playTick()

if (urlParams.has("file")) {
    document.getElementById("js-file").style.display = "none"

    fetch(urlParams.get("file"))
        .then(res => res.blob())
        .then(blob => blob.arrayBuffer())
        .then(buffer => observe(buffer))
}
