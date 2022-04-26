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
	Round                int
}

func main() {
	if len(os.Args) == 2 && os.Args[1] == "v" {
		fmt.Println("Proboj Tron Server")
		fmt.Println("version 11")
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

		res := DataToPlayer("HELLO", player.Name, "PREFLIGHT", scanner)
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
		fmt.Fprintf(os.Stderr, "ROUND %d\n", game.Round)

		// Read data from players
		commands := map[int]string{}
		for i, _ := range game.Players {
			player := &game.Players[i]
			if !player.Alive {
				continue
			}

			// Send state to player
			data := game.StateForPlayer(*player)
			res := DataToPlayer(data, player.Name, fmt.Sprintf("ROUND %d", game.Round), scanner)
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
			type affectedTile struct{ X, Y, Player int }
			affectedTiles := []affectedTile{}

			for i, _ := range game.Players {
				player := &game.Players[i]
				if !player.Alive {
					continue
				}

				if player.Speed == 0 || tick%(lcm/player.Speed) != 0 {
					continue
				}

				success, nx, ny := game.MovePlayer(player)

				// No collision
				if success {
					affectedTiles = append(affectedTiles, affectedTile{
						X:      player.X,
						Y:      player.Y,
						Player: player.Idx,
					})
					continue
				}

				// Collision with already standing wall
				// I die and update scores.
				game.HandleDeath(player)
				game.UpdateScore(player, nx, ny)
			}

			// Check player collisions.
			for i, _ := range game.Players {
				player := &game.Players[i]
				if !player.Alive {
					continue
				}

				// Check only players that moved this tick
				if player.Speed == 0 || tick%(lcm/player.Speed) != 0 {
					continue
				}

				playersHere := game.PlayersAt(player.X, player.Y)
				if len(playersHere) <= 1 {
					continue
				}

				// Multiple players ended up on the same tile. Kill them all.
				for _, p := range playersHere {
					game.HandleDeath(p)
				}
			}

			// Place tiles.
			for _, tile := range affectedTiles {
				game.Map.Contents[tile.X][tile.Y] = tile.Player
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
		if len(game.PlayersDeadThisRound) >= 1 {
			for _, p := range game.Players {
				if !p.Alive {
					continue
				}

				game.Scores[p.Name]++
			}
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

		game.Round++
	}
}
