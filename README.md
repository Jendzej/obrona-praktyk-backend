> # Backend i baza danych
> *Projekt na obronę praktyk*
>
Backend projektu, połączony z bazą danych, stworzony przy użyciu języka programowania *Python*, korzystając z takich
modułów jak:

- FastAPI,
- SQLAlchemy

## Uruchomienie projektu

___

### Baza danych

By uruchomić projekt lokalnie (przy użyciu Docker'a) należy zbudować obraz bazy danych używając poniższej komendy w
katalogu projektu:

```commandline
docker compose up -d --build
```

Po postawieniu bazy danych należy zamienić plik *pg_hba.conf*, który znajduje się w ./data/db, na ten znajdujący się w
katalogu ./src.

Po podmianie plików należy zrestartować kontener z bazą danych:

```commandline
docker compose restart
```

___

### Backend

Backend projektu należy uruchomić po uruchomieniu bazy danych.

## Commands

```
pipenv requirements > requirements.txt
```

Secret Key generation:

```
openssl rand -hex 32
```