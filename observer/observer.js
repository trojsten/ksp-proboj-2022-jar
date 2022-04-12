function setupCanvas(canvas) {
    let dpr = window.devicePixelRatio || 1
    let rect = canvas.getBoundingClientRect()
    canvas.width = rect.width * dpr
    canvas.height = rect.height * dpr
    let ctx = canvas.getContext('2d')
    ctx.scale(dpr, dpr)
    return ctx
}

const CANVAS = document.querySelector('.canvas')
const CTX = setupCanvas(CANVAS)
let GRID = 0
let OBSLINES = []
let FRAME = 0

function showFile(f) {
    let reader = new FileReader()
    reader.onload = function() {
        observe(reader.result)
    }
    reader.readAsText(f.files[0])
}

function observe(log) {
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
    setInterval(nextFrame, 100)
}

function nextFrame() {
    FRAME++
    if (FRAME < OBSLINES.length) {
        renderFrame(FRAME)
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
    GRID = CANVAS.width / frame.Map.Width
    CTX.clearRect(0, 0, CANVAS.width, CANVAS.height);

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
