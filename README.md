# Score App FastAPI

## Deploy as Docker container
```bash
$ docker-compose up
$ docker-compose up -d # Detached
```
The FastAPI endpoints will be reachable on 127.0.0.1:8000.

## Build Docker container
```bash
$ docker build .
```

## Run locally
```bash
$ uvicorn main:app --reload
```

## Create tables
```bash
$ python3 ./init/init_db.py
```

## View sqlite database locally

```bash
$ sudo apt install sqlitebrowser
$ sqlitebrowser db/score_app.db
```