package redis

import (
	"context"
	"strconv"
	"testing"

	"github.com/redis/go-redis/v9"
)

var testCtx = context.Background()
var testRdb = redis.NewClient(&redis.Options{
	Addr: "localhost:6379",
	DB:   15,
})

func TestRedisConnection(t *testing.T) {
	if err := testRdb.Ping(testCtx).Err(); err != nil {
		t.Fatalf("Redis connection failed: %v", err)
	}
}

func TestUserCreateAndGet(t *testing.T) {
	key := "test_user"
	testRdb.Del(testCtx, key)

	err := testRdb.Set(testCtx, key, 42, 0).Err()
	if err != nil {
		t.Fatalf("Failed to set value: %v", err)
	}

	val, err := testRdb.Get(testCtx, key).Result()
	if err != nil {
		t.Fatalf("Failed to get value: %v", err)
	}

	num, _ := strconv.Atoi(val)
	if num != 42 {
		t.Fatalf("Expected 42, got %d", num)
	}
}
