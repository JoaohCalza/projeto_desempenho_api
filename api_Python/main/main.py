from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3
from passlib.hash import bcrypt
from typing import List

app = FastAPI()

DB_FILE = "users.db"

# --------------------------
# Modelos Pydantic
# --------------------------
class User(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    user: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    user: str

# --------------------------
# Funções de banco
# --------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                user TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

init_db()

# --------------------------
# CRUD
# --------------------------
@app.post("/users", response_model=UserOut)
def create_user(user: User):
    hashed_password = bcrypt.hash(user.password[:72])
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, user, password) VALUES (?, ?, ?, ?)",
            (user.name, user.email, user.user, hashed_password)
        )
        conn.commit()
        user_id = c.lastrowid
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    return UserOut(id=user_id, name=user.name, email=user.email, user=user.user)

@app.get("/users", response_model=List[UserOut])
def get_users():
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT id, name, email, user FROM users")
        users = c.fetchall()
    finally:
        conn.close()
    return [UserOut(**dict(user)) for user in users]

@app.get("/users/{id}", response_model=UserOut)
def get_user(id: int):
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT id, name, email, user FROM users WHERE id = ?", (id,))
        user = c.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        conn.close()
    return UserOut(**dict(user))

@app.put("/users/{id}", response_model=UserOut)
def update_user(id: int, updated_user: User):
    hashed_password = bcrypt.hash(updated_user.password[:72])
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (id,))
        if not c.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        c.execute("""
            UPDATE users 
            SET name=?, email=?, user=?, password=? 
            WHERE id=?
        """, (updated_user.name, updated_user.email, updated_user.user, hashed_password, id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    return UserOut(id=id, name=updated_user.name, email=updated_user.email, user=updated_user.user)

@app.delete("/users/{id}")
def delete_user(id: int):
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (id,))
        if not c.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        c.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
    finally:
        conn.close()
    return {"message": "Deleted"}
