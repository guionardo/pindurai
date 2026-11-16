# PindurAí backend Go

Backend novo do PindurAí, isolado do Django/Quasar legado. Requer Go 1.27.4, Docker Compose e `golangci-lint` v2.

## Desenvolvimento local

```sh
docker compose up -d postgres
export DATABASE_URL='postgres://pindurai:pindurai-local-only@127.0.0.1:55433/pindurai?sslmode=disable'
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f migrations/0001_initial.sql
go run ./cmd/pindurai
curl http://127.0.0.1:8080/healthz
```

## Gates

```sh
make fix
make verify
make build
```

Não versionar credenciais, dados reais ou artefatos de build. O endpoint atual é somente um healthcheck; autenticação, domínio financeiro e sync entram nas próximas issues.
