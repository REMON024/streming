package cache

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
	"streaming/internal/config"
	"go.uber.org/zap"
)

type RedisClient struct {
	client *redis.Client
	logger *zap.Logger
}

func NewRedisClient(cfg *config.Config, logger *zap.Logger) *RedisClient {
	client := redis.NewClient(&redis.Options{
		Addr: cfg.RedisURL,
	})
	return &RedisClient{client: client, logger: logger}
}

func (r *RedisClient) Get(ctx context.Context, key string) (string, error) {
	return r.client.Get(ctx, key).Result()
}

func (r *RedisClient) Set(ctx context.Context, key, value string, ttl time.Duration) error {
	return r.client.Set(ctx, key, value, ttl).Err()
}

func (r *RedisClient) Del(ctx context.Context, key string) error {
	return r.client.Del(ctx, key).Err()
}
