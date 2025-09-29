package main

import (
	"context"
	"fmt"
	"strconv"

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
	if indicator == 0 {
		err := rdb.Set(ctx, username, 0, 0).Err()
		if err != nil {
			panic(err)
		}
		return true
	} else {
		return false
	}
}

func get_user_balance(username string) int {
	var indicator = check_exists(username)
	if indicator != 0 {
		balance, err := rdb.Get(ctx, username).Result()
		if err != nil {
			panic(err)
		}
		balanceInt, err := strconv.Atoi(balance)
		return int(balanceInt)
	} else {
		return 0
	}
}

func inc_user_balance(username string, bal int) bool {
	var ind = check_exists(username)
	if ind != 0 {
		b, err := rdb.Get(ctx, username).Result()
		if err != nil {
			panic(err)
		}
		balanceInt, err := strconv.Atoi(b)
		balanceInt += bal
		rdb.Set(ctx, username, balanceInt, 0)
		return true
	} else {
		return false
	}
}

func minus(username string, min int) bool {
	var ind = check_exists(username)
	if ind != 0 {
		b, err := rdb.Get(ctx, username).Result()
		if err != nil {
			panic(err)
		}
		bal, err := strconv.Atoi(b)
		if bal-min > 0 {
			rdb.Set(ctx, username, bal-min, 0)
			return true
		} else {
			fmt.Println("You dont have enough money")
			return false
		}
	} else {
		return false
	}
}
