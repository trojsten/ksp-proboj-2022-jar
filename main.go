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
	Color          string
	DisplayName    string
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
	populatePlayerData(&game, scanner)

	data, err := game.ObserverState()
	if err != nil {
		panic(err)
	}
	DataToObserver(data, scanner)

	gameLoop(&game, scanner)
	SendScores(game, scanner)
	fmt.Println("END\n.")
}

func populatePlayerData(game *Game, scanner *bufio.Scanner) {
	for i, _ := range game.Players {
		player := &game.Players[i]

		res := DataToPlayer("HELLO", player.Name, scanner)
		if res == Died {
			game.HandleDeath(player)
			continue
		}

		// Read data from player
		res, playerData := ReadFromPlayer(player.Name, scanner)
		if res == Died {
			game.HandleDeath(player)
			continue
		}

		_, err := fmt.Sscanf(playerData, "%s %s", &player.DisplayName, &player.Color)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
	}
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
				game.HandleDeath(player)
				continue
			}

			// Read data from player
			res, playerData := ReadFromPlayer(player.Name, scanner)
			if res == Died {
				game.HandleDeath(player)
				continue
			}

			// Update state
			valid := game.UpdateState(player, playerData)
			if !valid {
				KillPlayer(player.Name, scanner)
				game.HandleDeath(player)
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
