package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"time"
)

type Map struct {
	Width    int
	Height   int
	Contents [][]int
}

type Player struct {
	Idx            int
	Name           string
	X              int
	Y              int
	Dx             int
	Dy             int
	Speed          int
	SpeedResetTime int
	Alive          bool
}

type Game struct {
	Players     []Player
	Map         Map
	Scores      map[string]int
	PowerUps    []PowerUp
	PowerUpTime int
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	game := Game{}
	err := game.ReadConfig(scanner)
	if err != nil {
		panic(err)
	}

	rand.Seed(time.Now().UnixMilli())

	game.PrepareMap()
	data, err := game.ObserverState()
	if err != nil {
		panic(err)
	}
	DataToObserver(data, scanner)

	gameLoop(&game, scanner)
	SendScores(game, scanner)
	fmt.Println("END\n.")
}

func gameLoop(game *Game, scanner *bufio.Scanner) {
	for game.Running() {
		for i, _ := range game.Players {
			player := &game.Players[i]
			if !player.Alive {
				continue
			}

			// Send state to player
			data := game.StateForPlayer(*player)
			res := DataToPlayer(data, player.Name, scanner)
			if res == Died {
				player.Alive = false
				continue
			}

			// Read data from player
			res, playerData := ReadFromPlayer(player.Name, scanner)
			if res == Died {
				player.Alive = false
				continue
			}

			// Update state
			valid := game.UpdateState(player, playerData)
			if !valid {
				KillPlayer(player.Name, scanner)
				player.Alive = false
			}

			// Send state to observer
			data, err := game.ObserverState()
			if err != nil {
				panic(err)
			}
			DataToObserver(data, scanner)
		}

		game.PowerUpTime--
		if game.PowerUpTime < 0 {
			game.SpawnPowerUp()
			game.PowerUpTime = PUDefaultTime
		}
	}
}
