from datetime import date
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Depends, FastAPI, Form, Path
from pydantic import ValidationError
from sqlmodel import Session
from .garage import repo as garage_repo
from .car import repo as car_repo
from .maintenance import repo as maintanence_repo
from .schemas.GarageSchema import CreateGarage, UpdateGarage
from .schemas.CarSchema import CreateCar, UpdateCar, Car
from .schemas.MaintenanceSchema import CreateMaintenance, UpdateMaintenance, Maintenance
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
async def garages(db_session: session, city: str | None = None):
    if city:
        return garage_repo.get_garages_by_city(city, db_session)
    return garage_repo.get_garages(db_session)

@app.get("/garages/dailyAvailabilityReport")
async def get_garages_report(db_session: session,  startDate: date | None = None, endDate: date | None = None, garageId: int | None = None):
    return garage_repo.get_garages_report(garageId, startDate, endDate, db_session)

@app.post("/garages")
async def create_garage(data: Annotated[CreateGarage, Body()], db_session: session):
    garage_repo.create_garage(data, db_session)

@app.put("/garages/{id}")
async def update_garage(id, data: Annotated[UpdateGarage, Body()], db_session: session):
    garage_repo.update_garage(id, data, db_session)

@app.delete("/garages/{id}")
async def delete_garage(id, db_session: session):
    garage_repo.delete_garage(id, db_session)

## CARS

@app.get("/cars")
async def cars(db_session: session, carMake: str | None = None, fromYear: int | None = None, toYear: int | None = None, garageId: int | None = None):
    cars = []

    if carMake:
        for car in car_repo.get_cars_by_make(carMake, db_session):
            cars.append(Car.model_validate(car))
        return cars
    
    if fromYear and toYear:
        for car in car_repo.get_cars_by_year(fromYear, toYear, db_session):
            cars.append(Car.model_validate(car))
        return cars
    
    if garageId:
        for car in car_repo.get_cars_by_garage(garageId, db_session):
            cars.append(Car.model_validate(car))
        return cars
    
    if carMake is None and fromYear is None and toYear is None and garageId is None:
        for car in car_repo.get_cars(db_session):
            cars.append(Car.model_validate(car))

    return cars
    
@app.post("/cars")
async def create_car(data: Annotated[CreateCar, Body()], db_session: session):
    car_repo.create_car(data, db_session)

@app.put("/cars/{id}")
async def update_car(id, data: Annotated[UpdateCar, Body()], db_session: session):
    car_repo.update_car(id, data, db_session)

@app.delete("/cars/{id}")
async def delete_car(id, db_session: session):
    car_repo.delete_car(id, db_session)


## MAINTENANCE

@app.get("/maintenance")
async def maintenance(db_session: session, carId: int | None = None, startDate: date | None = None, endDate: date | None = None, garageId: int | None = None):
    maintenances = []

    if carId:
        for maintenance in maintanence_repo.get_maintenances_by_car(carId, db_session):
            maintenances.append(Maintenance.model_validate(maintenance))
        return maintenances
    
    if startDate and endDate:
        for maintenance in maintanence_repo.get_maintenances_by_date(startDate, endDate, db_session):
            maintenances.append(Maintenance.model_validate(maintenance))
        return maintenances
    
    if garageId:
        for maintenance in maintanence_repo.get_maintenances_by_garage(garageId, db_session):
            maintenances.append(Maintenance.model_validate(maintenance))
        return maintenances
    
    if carId is None and startDate is None and endDate is None and garageId is None:
        for maintenance in maintanence_repo.get_maintenances(db_session):
            maintenances.append(Maintenance.model_validate(maintenance))

    return maintenances

@app.post("/maintenance")
async def create_maintenance(data: Annotated[CreateMaintenance, Body()], db_session: session):
    maintanence_repo.create_maintenance(data, db_session)

@app.put("/maintenance/{id}")
async def update_car(id, data: Annotated[UpdateMaintenance, Body()], db_session: session):
    maintanence_repo.update_maintenance(id, data, db_session)

@app.delete("/maintenance/{id}")
async def delete_car(id, db_session: session):
    maintanence_repo.delete_maintenance(id, db_session)

@app.get("/maintenance/monthlyRequestsReport")
async def get_maintenance_monthlyReport(db_session: session, garageId: int | None = None, startMonth: str | None = None, endMonth: str | None = None):
    return maintanence_repo.get_maintenance_monthlyReport(garageId, startMonth, endMonth, db_session)