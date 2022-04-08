package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"math/rand"
	"strings"
)

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
	_, err := fmt.Sscanf(scanner.Text(), "%d %d", &g.Map.Width, &g.Map.Height)
	if err != nil {
		return err
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

	g.Map.Contents = make([][]int, g.Map.Width)
	for x := 0; x < g.Map.Width; x++ {
		g.Map.Contents[x] = make([]int, g.Map.Height)
		for y := 0; y < g.Map.Height; y++ {
			g.Map.Contents[x][y] = -1
		}
	}

	for i, _ := range g.Players {
		player := &g.Players[i]
		player.X = rand.Intn(g.Map.Width)
		player.Y = rand.Intn(g.Map.Height)
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
