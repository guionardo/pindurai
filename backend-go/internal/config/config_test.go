package config

import "testing"

func TestLoadRequiresDatabaseURL(t *testing.T) {
	t.Setenv("DATABASE_URL", "")

	if _, err := Load(); err == nil {
		t.Fatal("Load() error = nil, want missing DATABASE_URL error")
	}
}

func TestLoadUsesConfiguredValues(t *testing.T) {
	t.Setenv("DATABASE_URL", "postgres://localhost/pindurai")
	t.Setenv("PINDURAI_GO_ADDR", "127.0.0.1:18080")

	got, err := Load()
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}

	if got.DatabaseURL != "postgres://localhost/pindurai" {
		t.Errorf("DatabaseURL = %q", got.DatabaseURL)
	}
	if got.Address != "127.0.0.1:18080" {
		t.Errorf("Address = %q", got.Address)
	}
}
