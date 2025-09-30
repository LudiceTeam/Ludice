package data

import (
	"encoding/json"
	"os"
)

type Game struct {
	ID      string   `json:"id"`
	Players []string `json:"players"`
	Bet1    int      `json:"bet1"`
	Bet2    int      `json:"bet2"`
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
		ID:      "new_game",
		Players: []string{"new_player"},
		Bet1:    25,
		Bet2:    30,
		Res1:    0,
		Res2:    0,
	}

	existingGames = append(existingGames, newGame)

	jsonData, err := json.MarshalIndent(existingGames, "", "    ")
	if err != nil {
		panic(err)
	}

	err = os.WriteFile("data.json", jsonData, 0644)
	if err != nil {
		panic(err)
	}

}
