package main

import (
	"encoding/json"
	"os"

	"github.com/google/uuid"
)

type Game struct {
	ID      string   `json:"id"`
	Players []string `json:"players"`
	Bet     int      `json:"bet"`
	Res1    int      `json:"res1"`
	Res2    int      `json:"res2"`
}

func new_data() {
	data, err := os.ReadFile("game.json")
	if err != nil {
		panic(err)
	}
	var existingGames []Game
	err = json.Unmarshal(data, &existingGames)
	if err != nil {
		panic(err)
	}
	newGame := Game{
		ID:      uuid.New().String(),
		Players: []string{},
		Bet:     0,
		Res1:    0,
		Res2:    0,
	}

	existingGames = append(existingGames, newGame)

	jsonData, err := json.MarshalIndent(existingGames, "", "    ")
	if err != nil {
		panic(err)
	}

	err = os.WriteFile("game.json", jsonData, 0644)
	if err != nil {
		panic(err)
	}
}
func main() {
	for i := 0; i < 10; i++ {
		new_data()
	}
}
