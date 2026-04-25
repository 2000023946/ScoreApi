from fastapi import FastAPI
from pydantic import BaseModel
import dbm
import json

app = FastAPI()

DB_FILE = "scores.db"


class ScoreIn(BaseModel):
    score: int


def get_all_scores():
    with dbm.open(DB_FILE, "c") as db:
        return [json.loads(db[k].decode("utf-8")) for k in db.keys()]


def save_score(score: int):
    with dbm.open(DB_FILE, "c") as db:
        key = str(len(db))  # simple auto-increment key
        db[key] = json.dumps(score)


@app.post("/score")
def post_score(data: ScoreIn):
    save_score(data.score)
    return {"message": "score saved", "score": data.score}


@app.get("/top")
def get_top():
    scores = get_all_scores()
    top = sorted(scores, reverse=True)[:3]
    return {"top": top}