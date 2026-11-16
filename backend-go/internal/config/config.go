package config

import (
	"errors"
	"os"
)

const defaultAddress = "127.0.0.1:8080"

type Config struct {
	Address     string
	DatabaseURL string
}

func Load() (Config, error) {
	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		return Config{}, errors.New("DATABASE_URL is required")
	}

	address := os.Getenv("PINDURAI_GO_ADDR")
	if address == "" {
		address = defaultAddress
	}

	return Config{Address: address, DatabaseURL: databaseURL}, nil
}
