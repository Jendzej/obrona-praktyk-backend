# Backend and Database
### *School Project / Projekt na obronę praktyk*

---

 **_What is this project about?_**

This is backend of web application project - store with snacks and sandwiches with account for every client and completely functional admin site (adding, updating, deleting and managing items/users/transactions). 

---


> ## Technologies, functions and demo

### Technologies

Backend of bun-car site - project for school was created with **_Python (3.10)_** and modules like:

- FastAPI,
- SQLAlchemy

To store client data, transactions, items and other, I am using postgresql database.

### How it works?

Using Python module FastAPI, I created REST API for backend of my web application. To access database queries I designed specific endpoints, from which I can fetch and send data in my [frontend](https://github.com/Jendzej/obrona-praktyk-frontend).

Every endpoint work separately and asynchronously.

Example body and how looks endpoint for adding transactions:

![Add transaction](/docs/add_transaction.png)

... and how its code looks:

![Add transaction code](/docs/add_transaction_code.png)

Example query and how looks endpoint for deleting items:

![Delete items](/docs/delete_item.png)

... and how its code looks:

![Delete items code](/docs/delete_item_code.png)

In above examples You can see some type of endpoints visualisation, which actually is built-in FastAPI documentation (available on /docs).

### Logging

In this project you can find logger - it's not actually this what it should be. It just saves some useless info about running server and events; I didn't use it's potential.

---
## Starting

To start this part of project you must run database (for example locally on docker or somewhere on web) and specify database data in _.env_ file created on the [.env.example pattern](/.env.example).

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

1e1f5f612db705ab5f0fd2a1a8c91a03e3fa86fe28389a9393d8de8a748734b1

Start Database:

```
bash start_db.sh
```

Stop Database:

```
bash stop_db.sh
```
