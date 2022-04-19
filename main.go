package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

type Map struct {
	Width       int
	Height      int
	Contents    [][]int
	SpawnPoints []Point `json:"-"`
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
	PowerUp        PowerUpType
	Color          string
	DisplayName    string
}

type PowerUpActivation struct {
	Type   PowerUpType
	Player *Player
}

type Point struct {
	X, Y int
}

type Game struct {
	Players              []Player
	PlayersDeadThisRound []int               `json:"-"`
	PowerUpsThisRound    []PowerUpActivation `json:"-"`
	Map                  Map
	Scores               map[string]int
	PowerUps             []PowerUp
	PowerUpTime          int
}

func main() {
	if len(os.Args) == 2 && os.Args[1] == "v" {
		fmt.Println("Proboj Tron Server")
		fmt.Println("version 8")
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
		game.PowerUpsThisRound = []PowerUpActivation{}

		// Read data from players
		commands := map[int]string{}
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

			commands[player.Idx] = playerData
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

			data, exists := commands[player.Idx]
			if !exists {
				game.HandleDeath(player)
				continue
			}

			ok := game.RotatePlayer(player, data)
			if !ok {
				game.HandleDeath(player)
				continue
			}

			if strings.HasSuffix(data, "+") {
				if player.PowerUp != PUNone {
					game.PowerUpsThisRound = append(game.PowerUpsThisRound, PowerUpActivation{
						Type:   player.PowerUp,
						Player: player,
					})
					player.PowerUp = PUNone
				}
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

				if player.Speed == 0 {
					continue
				}

				if tick%(lcm/player.Speed) != 0 {
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

		// Apply powerups
		for _, activation := range game.PowerUpsThisRound {
			game.ApplyPowerUp(activation.Type, activation.Player)
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
