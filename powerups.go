package main

import "math/rand"

type PowerUpType int

type PowerUp struct {
	X    int
	Y    int
	Type PowerUpType
}

const PUTypeCount = 5
const PUDefaultTime = 10
const PUSpeedResetTime = 10

const (
	PUNone PowerUpType = iota
	PUSpeedMe
	PUSpeedOthers
	PUStopMe
	PUStopOthers
	PUClean
)

func (g *Game) ApplyPowerUp(typ PowerUpType, invoker *Player) {
	if typ == PUSpeedMe {
		invoker.Speed *= 2
		invoker.SpeedResetTime = PUSpeedResetTime
	} else if typ == PUSpeedOthers {
		for i, _ := range g.Players {
			player := &g.Players[i]
			if player == invoker {
				continue
			}

			player.Speed *= 2
			player.SpeedResetTime = PUSpeedResetTime
		}
	} else if typ == PUStopMe {
		invoker.Speed = 0
		invoker.SpeedResetTime = PUSpeedResetTime
	} else if typ == PUStopOthers {
		for i, _ := range g.Players {
			player := &g.Players[i]
			if player == invoker {
				continue
			}

			player.Speed = 0
			player.SpeedResetTime = PUSpeedResetTime
		}
	} else if typ == PUClean {
		for x := 0; x < g.Map.Width; x++ {
			for y := 0; y < g.Map.Height; y++ {
				g.Map.Contents[x][y] = -1
			}
		}
	}
}

func (g *Game) HasPowerUpAt(x, y int) bool {
	for _, up := range g.PowerUps {
		if up.X == x && up.Y == y {
			return true
		}
	}
	return false
}

func (g *Game) SpawnPowerUp() {
	x := rand.Intn(g.Map.Width)
	y := rand.Intn(g.Map.Height)

	tries := 0
	for g.Map.Contents[x][y] != -1 || g.HasPowerUpAt(x, y) {
		x = rand.Intn(g.Map.Width)
		y = rand.Intn(g.Map.Height)
		
		tries++
		if tries > 100 {
			return
		}
	}

	typ := 1 + rand.Intn(PUTypeCount)
	if g.Round >= g.Map.Width*g.Map.Height/len(g.Players)*3 {
		for PowerUpType(typ) == PUClean {
			typ = 1 + rand.Intn(PUTypeCount)
		}
	}

	g.PowerUps = append(g.PowerUps, PowerUp{
		X:    x,
		Y:    y,
		Type: PowerUpType(typ),
	})
}
