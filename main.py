import json
import sqlite3

from sqlite3 import Error
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

# NOTE: In case you run things locally, make sure the frontend runs on port 9000
origins = ["http://localhost:9000"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Tent(BaseModel):
    tentnr: int
    tentchef: str
    kampers: str


@app.delete("/tenten/{tentnr}")
def delete_tent(tentnr: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM tenten WHERE tentnr=%s;" % (tentnr))
    conn.commit()

    return {"ok": True}


@app.post("/tenten/")
def create_tent(tent: Tent):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("INSERT INTO tenten (tentnr, tentchef, kampers) VALUES (%s, '%s', '%s');" % (tent.tentnr, tent.tentchef, tent.kampers))
    conn.commit()

    return tent


@app.get("/tenten/{tentnr}")
def get_tent(tentnr: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM tenten WHERE tentnr='%s';" % tentnr)

    return {"tent": res.fetchone()}


@app.get("/tenten/")
def get_tenten():
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM tenten ORDER BY tentnr")

    return {"tenten": res.fetchall()}


class Activiteit(BaseModel):
    naam: str
    type: str
    dagdeel: str
    themadag_onderdeel: int


@app.delete("/activiteiten/{id}")
def delete_activiteit(id: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM activiteiten WHERE id=%s;" % (id))
    conn.commit()

    return {"ok": True}


@app.post("/activiteiten/")
def create_activiteit(activiteit: Activiteit):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("INSERT INTO activiteiten (naam, type, dagdeel, themadag_onderdeel) VALUES ('%s', '%s', '%s', %s);" % (
        activiteit.naam,
        activiteit.type,
        activiteit.dagdeel,
        activiteit.themadag_onderdeel
    ))
    conn.commit()

    return activiteit


@app.get("/activiteiten/{id}")
def get_activiteit(id: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM activiteiten WHERE id=%s;" % id)

    return {"activiteit": res.fetchone()}


@app.get("/activiteiten/")
def get_activiteiten():
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM activiteiten ORDER BY naam")

    return {"activiteiten": res.fetchall()}


class Uitslag(BaseModel):
    activiteit: str
    tentnr: int
    tentchef: str
    snelheid: str
    datum: str
    punten: int


@app.delete("/uitslagen/{tentnr}/{activiteit}")
def delete_uitslag(tentnr: int, activiteit: str):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM uitslagen WHERE tentnr=%s AND activiteit='%s';" % (tentnr, activiteit))
    conn.commit()

    return {"ok": True}


@app.post("/uitslagen/")
def create_uitslag(uitslag: Uitslag):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("INSERT INTO uitslagen (activiteit, tentnr, tentchef, snelheid, datum, punten) VALUES ('%s', '%s', '%s', '%s', '%s', %s);" % (
        uitslag.activiteit,
        uitslag.tentnr,
        uitslag.tentchef,
        uitslag.snelheid,
        uitslag.datum,
        uitslag.punten
    ))
    conn.commit()

    return uitslag


@app.get("/uitslagen/{id}")
def get_uitslag(id: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM uitslagen WHERE id=%s;" % id)

    return {"uitslagen": res.fetchone()}


@app.get("/uitslagen/")
def get_uitslagen():
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM uitslagen ORDER BY id DESC")

    return {"uitslagen": res.fetchall()}


class Score(BaseModel):
    tentnr: int
    score: int


@app.delete("/scores/{tentnr}")
def delete_score(tentnr: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM scores WHERE tentnr=%s;" % (tentnr))
    conn.commit()

    return {"ok": True}


@app.get("/scores/{tentnr}")
def get_score(tentnr: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM scores WHERE tentnr=%s;" % tentnr)

    return {"scores": res.fetchone()}


@app.get("/scores/")
def get_scores():
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM scores")

    return {"scores": res.fetchall()}


@app.put("/scores/{tentnr}")
def update_score(score: int, tentnr: int):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("UPDATE scores SET score = %s WHERE tentnr = %s" % (score, tentnr))
    conn.commit()

    return {"ok": True}


@app.post("/scores/")
def create_score(score: Score):
    conn = create_connection("db/score_app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (tentnr, score) VALUES (%s, %s);" % (score.tentnr, score.score))
    conn.commit()

    return score
