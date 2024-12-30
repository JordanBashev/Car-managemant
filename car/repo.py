from typing import Annotated
from fastapi import Depends
from sqlalchemy import delete, update
from sqlmodel import Session, select


from ..schemas.CarSchema import CreateCar, UpdateCar, Car as car
from ..db.db_connection import get_session
from ..db.models.cars import Car as CarModel
from ..db.models.car_to_garage import CarGarageLink

def get_cars(session: Annotated[Session, Depends(get_session)]):
    stmt = select(CarModel)
    cars = session.exec(stmt).all()
    return cars

def create_car(data: CreateCar, session: Annotated[Session, Depends(get_session)]):
    add_car = CarModel(make=data.make, model=data.model, licensePlate=data.licensePlate, productionYear=data.productionYear)
    session.add(add_car)
    session.commit()

    stmt = select(CarModel).where(CarModel.licensePlate == data.licensePlate)
    car = session.exec(stmt).one()

    for garage_id in data.garageIds:
        car_garage_link = CarGarageLink(car_id=car.id, garage_id=garage_id)
        session.add(car_garage_link)

    session.commit()


def update_car(id: int, data: UpdateCar, session: Annotated[Session, Depends(get_session)]):
    stmt = (update(CarModel).where(CarModel.id == id)
        .values(make=data.make, model=data.model, licensePlate=data.licensePlate, productionYear=data.productionYear))
    session.exec(stmt)

    stmt = select(CarModel).where(CarModel.licensePlate == data.licensePlate)
    car = session.exec(stmt).one()

    for garage_id in data.garageIds:
        statement = select(CarGarageLink).where(
            CarGarageLink.car_id == car.id,
            CarGarageLink.garage_id == garage_id
        )
        car_garage_link_existing = session.exec(statement).one_or_none()

        if car_garage_link_existing:
            stmt = (update(CarGarageLink).where(CarGarageLink.garage_id == car_garage_link_existing.garage_id)
                .values(garage_id == garage_id))
            session.exec(stmt)
        else:
            car_garage_link = CarGarageLink(car_id=car.id, garage_id=garage_id)
            session.add(car_garage_link)

    session.commit()

def delete_car(id: int, session: Annotated[Session, Depends(get_session)]):
    stmt_car = delete(CarModel).where(CarModel.id == id)
    session.exec(stmt_car)

    stmt_link = delete(CarGarageLink).where(CarGarageLink.car_id == id)
    session.exec(stmt_link)

    session.commit()

