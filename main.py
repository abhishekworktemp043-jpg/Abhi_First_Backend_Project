from fastapi import FastAPI, HTTPException
from Connect_database import get_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is my first API"}

from dotenv import load_dotenv

load_dotenv()

@app.get("/users")
def get_users():
    connection = get_connection()
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
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email, balance FROM users WHERE id = %s;", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": row[0], "name": row[1], "email": row[2], "balance": float(row[3])}

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    balance: float = 0

@app.post("/users")
def create_user(user: UserCreate):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, balance) VALUES (%s, %s, %s) RETURNING id;",
        (user.name, user.email, user.balance)
    )
    new_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return {"id": new_id, "name": user.name, "email": user.email, "balance": user.balance}

class UserUpdate(BaseModel):
    name: str
    email: str
    balance: float

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET name = %s, email = %s, balance = %s WHERE id = %s;",
        (user.name, user.email, user.balance, user_id)
    )
    updated_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user_id, "name": user.name, "email": user.email, "balance": user.balance}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    deleted_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user_id} deleted"}