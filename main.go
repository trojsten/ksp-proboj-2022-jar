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
	Players              []Player
	PlayersDeadThisRound []int
	Map                  Map
	Scores               map[string]int
	PowerUps             []PowerUp
	PowerUpTime          int
}

func main() {
	if len(os.Args) == 2 && os.Args[1] == "v" {
		fmt.Println("Proboj Tron Server")
		fmt.Println("version 3")
		return
	}

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
		game.PlayersDeadThisRound = []int{}

		// Read data from players
		commands := map[string]string{}
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

			commands[player.Name] = playerData
		}

		// Settle
		speeds := []int{}
		for i, _ := range game.Players {
			player := &game.Players[i]
			if !player.Alive {
				continue
			}

			if player.Speed != 0 {
				speeds = append(speeds, player.Speed)
			}

			data, exists := commands[player.Name]
			if !exists {
				game.HandleDeath(player)
				continue
			}

			ok := game.RotatePlayer(player, data)
			if !ok {
				game.HandleDeath(player)
				continue
			}
		}

		// Simulate movements
		lcm := LCM(speeds...)
		for tick := 1; tick <= lcm; tick++ {
			for i, _ := range game.Players {
				player := &game.Players[i]
				if !player.Alive {
					continue
				}

				if (lcm/player.Speed)%tick != 0 {
					continue
				}

				success, nx, ny := game.MovePlayer(player)
				if success {
					continue
				}

				// Collision, if with another player, kill him too.
				playerCollision := game.PlayerAt(nx, ny)
				if playerCollision != nil {
					game.HandleDeath(playerCollision)
				} else {
					// It was not player-player collision, so we update scores for that tile.
					game.UpdateScore(player, nx, ny)
				}
				game.HandleDeath(player)
				// TODO: Scores.
			}
		}

		// Update player times
		for i, _ := range game.Players {
			player := &game.Players[i]
			if !player.Alive {
				continue
			}

			game.SpeedTickPlayer(player)
		}

		// Update scores of players that died this round
		for _, n := range game.PlayersDeadThisRound {
			game.DeathScore(&game.Players[n])
		}

		// Send state to observer
		data, err := game.ObserverState()
		if err != nil {
			panic(err)
		}
		DataToObserver(data, scanner)

		game.PowerUpTime--
		if game.PowerUpTime < 0 {
			game.SpawnPowerUp()
			game.PowerUpTime = PUDefaultTime
		}
	}
}
