package config

import (
	"github.com/spf13/viper"
)

type Config struct {
	Port                string
	MinioEndpoint       string
	MinioAccessKey      string
	MinioSecretKey      string
	MinioUseSSL         bool
	RedisURL            string
	BackendURL          string
	JWTSecret           string
	JWTIssuer           string
	InternalAPIKey      string
	MaxTranscodeWorkers int
}

func Load() *Config {
	viper.AutomaticEnv()
	viper.SetDefault("PORT", "8080")
	viper.SetDefault("MAX_TRANSCODE_WORKERS", 3)
	viper.SetDefault("JWT_ISSUER", "streaming-platform")
	viper.SetDefault("MINIO_USE_SSL", false)

	return &Config{
		Port:                viper.GetString("PORT"),
		MinioEndpoint:       viper.GetString("MINIO_ENDPOINT"),
		MinioAccessKey:      viper.GetString("MINIO_ACCESS_KEY"),
		MinioSecretKey:      viper.GetString("MINIO_SECRET_KEY"),
		MinioUseSSL:         viper.GetBool("MINIO_USE_SSL"),
		RedisURL:            viper.GetString("REDIS_URL"),
		BackendURL:          viper.GetString("BACKEND_URL"),
		JWTSecret:           viper.GetString("JWT_SECRET"),
		JWTIssuer:           viper.GetString("JWT_ISSUER"),
		InternalAPIKey:      viper.GetString("INTERNAL_API_KEY"),
		MaxTranscodeWorkers: viper.GetInt("MAX_TRANSCODE_WORKERS"),
	}
}
