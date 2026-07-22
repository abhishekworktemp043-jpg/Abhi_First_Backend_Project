from fastapi import FastAPI, HTTPException
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is my first API"}

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

@app.get("/users")
def get_users():
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email, balance FROM users;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    users = []
    for row in rows:
        users.append({"id": row[0], "name": row[1], "email": row[2], "balance": float(row[3])})

    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email, balance FROM users WHERE id = %s;", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": row[0], "name": row[1], "email": row[2], "balance": float(row[3])}