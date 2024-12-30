from typing import Annotated
from fastapi import Depends
from sqlalchemy import delete, update
from sqlmodel import Session, select

from ..schemas.GarageSchema import CreateGarage, UpdateGarage, Garage as garage
from ..db.db_connection import get_session
from ..db.models.garage import Garage as GarageModel

def get_garages(session: Annotated[Session, Depends(get_session)]):
    stmt = select(GarageModel)
    garages = session.exec(stmt).all()
    return garages

def get_garages_by_city(city: str, session: Annotated[Session, Depends(get_session)]):
    stmt = select(GarageModel).where(GarageModel.city == city)
    garages = session.exec(stmt).all()
    return garages

def create_garage(data: CreateGarage, session: Annotated[Session, Depends(get_session)]):
    add_garage = GarageModel(name=data.name, location=data.location, city=data.city, capacity=data.capacity)
    session.add(add_garage)
    session.commit()

def update_garage(id: int, data: UpdateGarage, session: Annotated[Session, Depends(get_session)]):
    stmt = (update(GarageModel).where(GarageModel.id == id)
        .values(name=data.name, location=data.location, capacity=data.capacity, city=data.city))
    session.exec(stmt)
    session.commit()

def delete_garage(id: int, session: Annotated[Session, Depends(get_session)]):
    stmt = delete(GarageModel).where(GarageModel.id == id)
    session.exec(stmt)
    session.commit()

def seed(session: Annotated[Session, Depends(get_session)]):
    add_garage = GarageModel(name="test", location="test", city="test", capacity=2)
    session.add(add_garage)
    session.commit()
    