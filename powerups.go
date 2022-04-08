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

const (
	PUSpeedMe PowerUpType = iota
	PUSpeedOthers
	PUStopMe
	PUStopOthers
	PUClean
)

func (g *Game) ApplyPowerUp(typ PowerUpType, invoker *Player) {
	if typ == PUSpeedMe {
		invoker.Speed *= 2
		invoker.SpeedResetTime = 10
	} else if typ == PUSpeedOthers {
		for i, _ := range g.Players {
			player := &g.Players[i]
			if player == invoker {
				continue
			}

			player.Speed *= 2
			player.SpeedResetTime = 10
		}
	} else if typ == PUStopMe {
		invoker.Speed = 0
		invoker.SpeedResetTime = 10
	} else if typ == PUStopOthers {
		for i, _ := range g.Players {
			player := &g.Players[i]
			if player == invoker {
				continue
			}

			player.Speed = 0
			player.SpeedResetTime = 10
		}
	} else if typ == PUClean {
		for x := 0; x < g.Map.Width; x++ {
			for y := 0; y < g.Map.Height; y++ {
				g.Map.Contents[x][y] = -1
			}
		}
	}
}

func (g *Game) SpawnPowerUp() {
	x := rand.Intn(g.Map.Width)
	y := rand.Intn(g.Map.Height)

	g.PowerUps = append(g.PowerUps, PowerUp{
		X:    x,
		Y:    y,
		Type: PowerUpType(rand.Intn(PUTypeCount)),
	})
}
