from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Render provides this automatically
DATABASE_URL = os.environ.get("DATABASE_URL")
# Create connection
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True  # simplifies things for this small project


# Initialize table
def init_db():
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            score INT NOT NULL
        )
        """)

init_db()


class ScoreIn(BaseModel):
    score: int


@app.post("/score")
def post_score(data: ScoreIn):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO scores (score) VALUES (%s)",
            (data.score,)
        )
    return {"message": "score saved", "score": data.score}


@app.get("/top")
def get_top():
    with conn.cursor() as cur:
        cur.execute(
            "SELECT score FROM scores ORDER BY score DESC LIMIT 3"
        )
        rows = cur.fetchall()

    return {"top": [r[0] for r in rows]}