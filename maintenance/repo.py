from datetime import date, timedelta
from typing import Annotated
from fastapi import Depends
from sqlalchemy import delete, func, update
from sqlmodel import Session, select


from ..schemas.MaintenanceSchema import CreateMaintenance, MaintenanceMonthlyReport, UpdateMaintenance, Maintenance as maintanance
from ..db.db_connection import get_session
from ..db.models.maintenance import Maintenance as MaintenanceModel
from ..db.models.car_to_garage import CarGarageLink
from ..db.models.garage import Garage
from ..db.models.cars import Car

def get_maintenances(session: Annotated[Session, Depends(get_session)]):
    stmt = select(MaintenanceModel)
    maintenances = session.exec(stmt).all()
    return maintenances

def get_maintenances_by_car(carId: int, session: Annotated[Session, Depends(get_session)]):
    stmt = select(MaintenanceModel).where(MaintenanceModel.carId == carId)
    maintenances = session.exec(stmt).all()
    return maintenances

def get_maintenances_by_garage(garageId: int, session: Annotated[Session, Depends(get_session)]):
    stmt = select(MaintenanceModel).where(MaintenanceModel.garageId == garageId)
    maintenances = session.exec(stmt).all()
    return maintenances

def get_maintenances_by_date(startYear: date, endYear: date, session: Annotated[Session, Depends(get_session)]):
    stmt = select(MaintenanceModel).where(MaintenanceModel.scheduledDate >= startYear, 
                                          MaintenanceModel.scheduledDate <= endYear)
    maintenances = session.exec(stmt).all()
    return maintenances

def get_maintenance_monthlyReport(garageId: int, startYear: date, endYear: date, session: Annotated[Session, Depends(get_session)]):
    start_date = date.fromisoformat(f"{startYear}-01")
    year, month = map(int, endYear.split("-"))
    
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    stmt = (
        select(
            func.strftime("%Y-%m", MaintenanceModel.scheduledDate).label("yearMonth"),
            func.count(MaintenanceModel.id).label("requests")
        )
        .where(
            MaintenanceModel.scheduledDate >= start_date,
            MaintenanceModel.scheduledDate <= end_date,
            MaintenanceModel.garageId == garageId
        )
        .group_by(func.strftime("%Y-%m", MaintenanceModel.scheduledDate))
        .order_by("yearMonth")
    )

    results = session.exec(stmt).all()

    reports = [
        MaintenanceMonthlyReport(yearMonth=row.yearMonth, requests=row.requests)
        for row in results
    ]
    return reports

    
def create_maintenance(data: CreateMaintenance, session: Annotated[Session, Depends(get_session)]):

    stmt = select(Garage).where(Garage.id == data.garageId)
    garage_capacity = session.exec(stmt).one().capacity

    statmt = select(CarGarageLink).where(CarGarageLink.garage_id == data.garageId)
    cars_in_garage = session.exec(statmt).all()

    if garage_capacity <= len(cars_in_garage):
        return 1

    add_maintenance = MaintenanceModel(serviceType=data.serviceType, scheduledDate=data.scheduledDate, carId=data.carId, garageId=data.garageId)
    session.add(add_maintenance)
    session.commit()


def update_maintenance(id: int, data: UpdateMaintenance, session: Annotated[Session, Depends(get_session)]):
    stmt = (update(MaintenanceModel).where(MaintenanceModel.id == id)
        .values(serviceType=data.serviceType, scheduledDate=data.scheduledDate, carId=data.carId, garageId=data.garageId))
    session.exec(stmt)
    session.commit()

def delete_maintenance(id: int, session: Annotated[Session, Depends(get_session)]):
    stmt_maintenance = delete(MaintenanceModel).where(MaintenanceModel.id == id)
    session.exec(stmt_maintenance)
    session.commit()

# def seed(session: Annotated[Session, Depends(get_session)]):
#     add_maintenance = maintenanceModel(make="test", model="test", licensePlate="test", productionYear=325)
#     session.add(add_maintenance)
#     session.commit()
    