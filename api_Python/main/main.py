from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ---- MODEL ----
class User(BaseModel):
    id: int | None = None
    name: str
    email: str

# ---- BANCO EM MEMÓRIA (somente para testes) ----
users_db = []
next_id = 1

# ---- CREATE ----
@app.post("/users")
def create_user(user: User):
    global next_id
    user.id = next_id
    next_id += 1
    users_db.append(user)
    return user

# ---- READ ALL ----
@app.get("/users")
def get_users():
    return users_db

# ---- READ BY ID ----
@app.get("/users/{id}")
def get_user(id: int):
    for user in users_db:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# ---- UPDATE ----
@app.put("/users/{id}")
def update_user(id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if user.id == id:
            updated_user.id = id
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# ---- DELETE ----
@app.delete("/users/{id}")
def delete_user(id: int):
    for i, user in enumerate(users_db):
        if user.id == id:
            deleted = users_db.pop(i)
            return deleted
    raise HTTPException(status_code=404, detail="User not found")
