package main

import (
	"fmt"
	"strconv"
	"strings"
)

func (g Game) Running() bool {
	alive := 0
	for _, player := range g.Players {
		if player.Alive {
			alive++
		}
	}

	return alive > 1
}

func (g Game) StateForPlayer(p Player) string {
	data := []string{}
	// Map width, height
	data = append(data, fmt.Sprintf("%d %d", g.Map.Width, g.Map.Height))

	// Map layout
	for y := 0; y < g.Map.Height; y++ {
		row := []string{}
		for x := 0; x < g.Map.Width; x++ {
			if g.Map.Contents[x][y] == -1 {
				row = append(row, "0")
			} else {
				row = append(row, "1")
			}
		}
		data = append(data, strings.Join(row, " "))
	}

	// Myself
	data = append(data, fmt.Sprintf("1 %d %d %d %d %d %d %d", p.X, p.Y, p.Dx, p.Dy, p.Speed, p.SpeedResetTime, p.PowerUp))

	// Players (excl. me)
	data = append(data, strconv.Itoa(len(g.Players)-1))
	for _, player := range g.Players {
		if player.Name == p.Name {
			continue
		}

		var aliveInt int
		if p.Alive {
			aliveInt = 1
		} else {
			aliveInt = 0
		}
		data = append(data, fmt.Sprintf("%d %d %d %d %d %d 0 0", aliveInt, player.X, player.Y, player.Dx, player.Dy, player.Speed))
	}

	// Power-ups
	data = append(data, strconv.Itoa(len(g.PowerUps)))
	for _, up := range g.PowerUps {
		data = append(data, fmt.Sprintf("%d %d", up.X, up.Y))
	}

	return strings.Join(data, "\n")
}

func (g *Game) PlayerAt(x, y int) *Player {
	if x < 0 || y < 0 || x >= g.Map.Width || y >= g.Map.Height {
		return nil
	}

	for i, _ := range g.Players {
		player := &g.Players[i]
		if !player.Alive {
			continue
		}

		if player.X == x && player.Y == y {
			return player
		}
	}

	return nil
}

func (g *Game) HandleDeath(p *Player) {
	p.Alive = false
	g.PlayersDeadThisRound = append(g.PlayersDeadThisRound, p.Idx)
}

func (g *Game) UpdateScore(p *Player, x, y int) {
	// Out-of-bounds
	if x < 0 || y < 0 || x >= g.Map.Width || y >= g.Map.Height {
		return
	}

	tile := g.Map.Contents[x][y]

	// Empty tiles
	if tile == -1 {
		return
	}

	// My own tile
	if tile == p.Idx {
		g.Scores[p.Name]--
		return
	}

	// Tile of another player
	if tile >= 0 {
		g.Scores[g.Players[tile].Name]++
	}
}

func (g *Game) DeathScore(p *Player) {
	alive := []Player{}
	for _, player := range g.Players {
		if player.Alive {
			alive = append(alive, player)
		}
	}

	if len(alive) == 1 {
		g.Scores[alive[0].Name] += len(g.Players)
	}

	g.Scores[p.Name] += len(g.Players) - len(alive)
}
