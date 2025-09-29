package main

import (
	"context"
	"fmt"
	"strconv"

	"net/http"

	"github.com/gin-gonic/gin"
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

type INC struct {
	username string `json:"username" binding:"required"`
	money    int    `json:"inc_money" binding:"required"`
}

func main() {
	r := gin.Default()
	r.GET("/user/:username/create", func(c *gin.Context) {
		username := c.Param("username")
		set_user_balance(username)
		c.JSON(http.StatusOK, gin.H{
			"DONE": "OK",
		})
	})
	r.GET("/get/:username/balance", func(c *gin.Context) {
		username := c.Param("username")
		var balance int = get_user_balance(username)
		c.JSON(http.StatusOK, gin.H{
			"Balance": balance,
		})
	})
	r.POST("/increase", func(c *gin.Context) {
		var increse_class INC
		if err := c.ShouldBindJSON(&increse_class); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "Wrong data",
			})
			return
		}
		var incr bool = inc_user_balance(increse_class.username, increse_class.money)
		if incr {
			c.Status(200)
			return
		} else {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "Something went wrong",
			})
			return
		}

	})
	r.POST("/minus", func(c *gin.Context) {
		var minus_class INC
		if err := c.ShouldBindJSON(&minus_class); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "Wrong data",
			})
			return
		}
		var indic bool = minus(minus_class.username, minus_class.money)
		if indic {
			c.Status(200)
		} else {
			c.JSON(http.StatusBadGateway, gin.H{
				"error": "You dont have enought money",
			})
			return
		}
	})

	r.Run(":8000")
}
