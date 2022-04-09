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
	data = append(data, fmt.Sprintf("1 %d %d %d %d %d %d", p.X, p.Y, p.Dx, p.Dy, p.Speed, p.SpeedResetTime))

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
		data = append(data, fmt.Sprintf("%d %d %d %d %d %d 0", aliveInt, player.X, player.Y, player.Dx, player.Dy, player.Speed))
	}

	// Power-ups
	data = append(data, strconv.Itoa(len(g.PowerUps)))
	for _, up := range g.PowerUps {
		data = append(data, fmt.Sprintf("%d %d", up.X, up.Y))
	}

	return strings.Join(data, "\n")
}

func (g *Game) UpdateState(p *Player, data string) bool {
	newDx := 0
	newDy := 0

	if data == "L" {
		newDx = p.Dy
		newDy = -p.Dx
	} else if data == "R" {
		newDx = -p.Dy
		newDy = p.Dx
	} else if data == "x" {
		newDx = p.Dx
		newDy = p.Dy
	} else {
		return false
	}

	for i := 1; i < p.Speed+1; i++ {
		x := p.X + newDx*i
		y := p.Y + newDy*i
		if x < 0 || y < 0 || x >= g.Map.Width || y >= g.Map.Height {
			return false
		}

		tile := &g.Map.Contents[x][y]
		if *tile != -1 {
			if *tile >= 0 {
				if *tile != p.Idx {
					g.Scores[g.Players[*tile].Name]++
				} else {
					g.Scores[p.Name]--
				}
			}
			return false
		}
		*tile = p.Idx

		for i, up := range g.PowerUps {
			if up.X == x && up.Y == y {
				g.ApplyPowerUp(up.Type, p)
				g.PowerUps = append(g.PowerUps[:i], g.PowerUps[i+1:]...)
				break
			}
		}
	}

	p.X = p.X + newDx*p.Speed
	p.Y = p.Y + newDy*p.Speed
	p.Dx = newDx
	p.Dy = newDy

	if p.Speed != 1 {
		p.SpeedResetTime--
		if p.SpeedResetTime <= 0 {
			p.Speed = 1
		}
	}

	return true
}

func (g *Game) HandleDeath(p *Player) {
	p.Alive = false

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
