package main

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()
var rdb = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       0,
})

func init() {

	err := rdb.Ping(ctx).Err()
	if err != nil {
		panic(err)
	}
	fmt.Println("Connected to Redis")
}

func check_exists(username string) int {
	exists1, err := rdb.Exists(ctx, username).Result()
	if err != nil {
		panic(err)
	}
	return int(exists1)

}

func set_user_balance(username string) bool {
	var indicator = check_exists(username)
	if indicator != 0 {
		err := rdb.Set(ctx, username, 0, 0).Err()
		if err != nil {
			panic(err)
		}
		return true
	} else {
		return false
	}
}
