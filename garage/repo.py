from datetime import date, timedelta
from typing import Annotated
from fastapi import Depends
from sqlalchemy import delete, func, update
from sqlmodel import Session, select

from ..schemas.GarageSchema import CreateGarage, UpdateGarage, GarageReport, Garage as garage
from ..db.db_connection import get_session
from ..db.models.garage import Garage as GarageModel
from ..db.models.maintenance import Maintenance as MaintenanceModel

def get_garages(session: Annotated[Session, Depends(get_session)]):
    stmt = select(GarageModel)
    garages = session.exec(stmt).all()
    return garages

def get_garages_by_city(city: str, session: Annotated[Session, Depends(get_session)]):
    stmt = select(GarageModel).where(GarageModel.city == city)
    garages = session.exec(stmt).all()
    return garages

def get_garages_report(garageId: int, startDate: date, endDate: date, session: Annotated[Session, Depends(get_session)]):
    garage_stmt = select(GarageModel.capacity).where(GarageModel.id == garageId)
    garage_capacity = session.exec(garage_stmt).one_or_none()

    if garage_capacity is None:
        return 1

    date_range = [startDate + timedelta(days=i) for i in range((endDate - startDate).days + 1)]

    reports = []

    for day in date_range:
        maintenance_stmt = (
            select(func.count(MaintenanceModel.id))
            .where(
                MaintenanceModel.scheduledDate == day,
                MaintenanceModel.garageId == garageId
            )
        )
        requests = session.exec(maintenance_stmt).one_or_none()

        if requests is None:
            return 1
        
        availableCapacity = max(0, garage_capacity - requests)

        reports.append(GarageReport(date=day, requests=requests, availableCapacity=availableCapacity))
    
    return reports

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
    