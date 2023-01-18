# Backend and Database
### *School Project / Projekt na obronę praktyk*

---

 **_What is this project about?_**

This is backend of web application project - store with snacks and sandwiches with account for every client and completely functional admin site (adding, updating, deleting and managing items/users/transactions). 

---


> ## Technologies, functions and demo

## Technologies

Backend of bun-car site - project for school was created with **_Python (3.10)_** and modules like:

- FastAPI,
- SQLAlchemy

To store client data, transactions, items and other, I am using postgresql database.

## How it works?

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
> ## Starting
> How to start and setup backend

To start this part of project, firstly, you must run database (for example locally on docker or somewhere on web).

While database is running, You can set up all environment variables in **_.env_** file on [.env.example pattern](/.env.example).

|          Variable           | Description                                                                                                                            |
|:---------------------------:|----------------------------------------------------------------------------------------------------------------------------------------|
|         POSTGRES_DB         | Name of database                                                                                                                       |
|        POSTGRES_USER        | Username to postgres administrator                                                                                                     |
|      POSTGRES_PASSWORD      | Password to postgres administrator                                                                                                     |
|        POSTGRES_HOST        | IP of database host                                                                                                                    |
|        POSTGRES_PORT        | Port of database host                                                                                                                  |
|         SECRET_KEY          | Secret key used to data encryption (32bytes hex string ([OpenSSL docs](https://www.openssl.org/docs/man1.0.2/man1/openssl-rand.html))) |
|          ALGORITHM          | Algorithm used for data encryption (HS256)                                                                                             |
| ACCESS_TOKEN_EXPIRE_MINUTES | Time to JWT token expiry                                                                                                               |
|     PAGE_ADMIN_USERNAME     | Username to admin account (user which is created on startup with admin role)                                                           |
|     PAGE_ADMIN_PASSWORD     | Password to admin account                                                                                                              |
|      PAGE_ADMIN_EMAIL       | Admin account email                                                                                                                    |

If you have filled-up **_.env_** file, You must install python packages:

```commandline
pip install -r requirements.txt
```

... And then (finally), You can run backend:
```commandline
python main.py
```

Now REST API should be available on localhost or server IP on port 8000 http://127.0.0.1:8000.
