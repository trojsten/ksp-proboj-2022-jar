package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"image/png"
	"math/rand"
	"os"
	"path"
	"strings"
)

func (m *Map) SpawnPoint() (Point, error) {
	if len(m.SpawnPoints) == 0 {
		return Point{}, fmt.Errorf("not enough spawnpoints available")
	}

	i := rand.Intn(len(m.SpawnPoints))
	sp := m.SpawnPoints[i]
	m.SpawnPoints = append(m.SpawnPoints[:i], m.SpawnPoints[i+1:]...)
	return sp, nil
}

func (g *Game) LoadMap(file string) error {
	f, err := os.OpenFile(path.Join("maps", file), os.O_RDONLY, os.ModePerm)
	if err != nil {
		return err
	}
	defer f.Close()

	imData, err := png.Decode(f)
	if err != nil {
		return err
	}
	g.Map.Width = imData.Bounds().Size().X
	g.Map.Height = imData.Bounds().Size().Y

	g.Map.Contents = make([][]int, g.Map.Width)
	for x := 0; x < g.Map.Width; x++ {
		g.Map.Contents[x] = make([]int, g.Map.Height)
		for y := 0; y < g.Map.Height; y++ {
			g.Map.Contents[x][y] = -1
			color := imData.At(imData.Bounds().Min.X+x, imData.Bounds().Min.Y+y)
			r, gr, b, _ := color.RGBA()

			if r == 65535 && gr == 0 && b == 0 {
				g.Map.SpawnPoints = append(g.Map.SpawnPoints, Point{
					X: x,
					Y: y,
				})
			} else if r == 65535 && gr == 65535 && b == 65535 {
				g.Map.Contents[x][y] = -2
			}
		}
	}

	return nil
}

func (g *Game) GenerateMap() {
	g.Map.Contents = make([][]int, g.Map.Width)
	for x := 0; x < g.Map.Width; x++ {
		g.Map.Contents[x] = make([]int, g.Map.Height)
		for y := 0; y < g.Map.Height; y++ {
			g.Map.Contents[x][y] = -1
			g.Map.SpawnPoints = append(g.Map.SpawnPoints, Point{
				X: x,
				Y: y,
			})
		}
	}
}

func (g *Game) ReadConfig(scanner *bufio.Scanner) error {
	scanner.Scan()
	data := scanner.Text()
	if data != "CONFIG" {
		return fmt.Errorf("error reading from runner: expected 'CONFIG', got '%v'", data)
	}

	scanner.Scan()
	g.Scores = map[string]int{}
	players := strings.Split(scanner.Text(), " ")
	for i, player := range players {
		g.Players = append(g.Players, Player{
			Name: player,
			Idx:  i,
		})
		g.Scores[player] = 0
	}

	scanner.Scan()
	data = scanner.Text()
	if strings.Contains(data, ".png") {
		err := g.LoadMap(data)
		if err != nil {
			return err
		}
	} else {
		_, err := fmt.Sscanf(data, "%d %d", &g.Map.Width, &g.Map.Height)
		if err != nil {
			return err
		}

		g.GenerateMap()
	}

	scanner.Scan()
	data = scanner.Text()
	if data != "." {
		return fmt.Errorf("error reading from runner: expected end of input, got '%v'", data)
	}

	return nil
}

var directions = [][]int{
	{0, 1}, {0, -1}, {1, 0}, {-1, 0},
}

func (g *Game) PrepareMap() {
	g.PowerUpTime = PUDefaultTime
	g.PowerUps = []PowerUp{}

	for i, _ := range g.Players {
		player := &g.Players[i]
		sp, err := g.Map.SpawnPoint()
		if err != nil {
			panic(err)
		}

		player.X = sp.X
		player.Y = sp.Y
		g.Map.Contents[player.X][player.Y] = player.Idx
		player.Alive = true

		direction := directions[rand.Intn(4)]
		player.Dx = direction[0]
		player.Dy = direction[1]
		player.Speed = 1
	}
}

func (g Game) ObserverState() (string, error) {
	data, err := json.Marshal(g)
	return string(data), err
}
