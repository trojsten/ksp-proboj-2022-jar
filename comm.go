package main

import (
	"bufio"
	"fmt"
	"strings"
)

type ServerResult int

const (
	Ok ServerResult = iota
	Unknown
	Died
)

func DataToObserver(data string, server *bufio.Scanner) ServerResult {
	fmt.Println("TO OBSERVER")
	fmt.Println(data)
	fmt.Println(".")

	server.Scan()
	res := server.Text()
	if res == "OK" {
		return Ok
	}
	return Unknown
}

func DataToPlayer(data string, player string, server *bufio.Scanner) ServerResult {
	fmt.Printf("TO PLAYER %s\n", player)
	fmt.Println(data)
	fmt.Println(".")

	server.Scan()
	res := server.Text()
	if res == "OK" {
		return Ok
	} else if res == "DIED" {
		return Died
	}
	return Unknown
}

func ReadFromPlayer(player string, server *bufio.Scanner) (ServerResult, string) {
	fmt.Printf("READ PLAYER %s\n", player)
	fmt.Println(".")

	server.Scan()
	res := server.Text()
	if res == "OK" {
		result := []string{}
		for true {
			server.Scan()
			input := server.Text()
			if input == "." {
				break
			}
			result = append(result, input)
		}
		return Ok, strings.Join(result, "\n")
	} else if res == "DIED" {
		return Died, ""
	}
	return Unknown, ""
}

func KillPlayer(player string, server *bufio.Scanner) ServerResult {
	fmt.Printf("KILL PLAYER %s\n", player)
	fmt.Println(".")

	server.Scan()
	res := server.Text()
	if res == "OK" {
		return Ok
	}
	return Unknown
}

func SendScores(game Game, server *bufio.Scanner) ServerResult {
	fmt.Println("SCORES")
	for player, score := range game.Scores {
		fmt.Printf("%s %d\n", player, score)
	}
	fmt.Println(".")

	server.Scan()
	res := server.Text()
	if res == "OK" {
		return Ok
	}
	return Unknown
}
