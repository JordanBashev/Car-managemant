from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Depends, FastAPI, Form
from sqlmodel import Session
from .garage import repo as garage_repo
from .schemas.GarageSchema import CreateGarage, UpdateGarage
from .db.db_connection import get_session

from .db.db_connection import create_db_and_tables

create_db_and_tables()

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8088",
    "http://127.0.0.1:8088",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = Annotated[Session, Depends(get_session)]

## GARAGES

@app.get("/garages")
async def garages(db_session: session):
    return garage_repo.get_garages(db_session)

@app.post("/garages")
async def create_garage(data: Annotated[CreateGarage, Body()], db_session: session):
    garage_repo.create_garage(data, db_session)

@app.put("/garages/{id}")
async def update_garage(id, data: Annotated[UpdateGarage, Body()], db_session: session):
    garage_repo.update_garage(id, data, db_session)

@app.delete("/garages/{id}")
async def root(id, db_session: session):
    garage_repo.delete_garage(id, db_session)

# @app.get("/garages")
# async def root():
#     print("data")