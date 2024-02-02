import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    logger.info('Отработал GET запрос.')
    return {"message": "Start page"}


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    status: str


users = []


@app.get("/users/", response_model=list[User])
async def read_user():
    logger.info('Отработал POST запрос.')
    return users


@app.get("/user/{user_id}/", response_model=User)
async def create_item(user_id: int):
    for user in users:
        if user.id == user_id:
            logger.info('Отработал POST запрос.')
            return user
        return HTTPException(status_code=404, detail="User not found")


@app.post("/user/", response_model=User)
async def create_user(user: User):
    users.append(user)
    logger.info('Отработал POST запрос.')
    return user


@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    for i, user_ in enumerate(users):
        if user_.id == user_id:
            users[i] = user
            logger.info(f'Отработал PUT запрос для user id = {user_id}.')
            return user
        return HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i].status = "deleted"
            logger.info(f'Отработал PUT запрос для user id = {user_id}.')
            return user
        return HTTPException(status_code=404, detail="User not found")