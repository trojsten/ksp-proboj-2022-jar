package main

func (g *Game) RotatePlayer(p *Player, data string) bool {
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

	p.Dx = newDx
	p.Dy = newDy
	return true
}

func (g *Game) MovePlayer(p *Player) (bool, int, int) {
	x := p.X + p.Dx
	y := p.Y + p.Dy

	if x < 0 || y < 0 || x >= g.Map.Width || y >= g.Map.Height {
		return false, x, y
	}

	tile := &g.Map.Contents[x][y]
	if *tile != -1 {
		return false, x, y
	}
	*tile = p.Idx

	p.X = x
	p.Y = y

	// Todo pickup
	for i, up := range g.PowerUps {
		if up.X == x && up.Y == y {
			g.PowerUpsThisRound = append(g.PowerUpsThisRound, PowerUpActivation{
				Type:   up.Type,
				Player: p,
			})
			g.PowerUps = append(g.PowerUps[:i], g.PowerUps[i+1:]...)
			break
		}
	}

	return true, x, y
}

func (g *Game) SpeedTickPlayer(p *Player) {
	if p.Speed != 1 {
		p.SpeedResetTime--
		if p.SpeedResetTime <= 0 {
			p.Speed = 1
		}
	}
}
