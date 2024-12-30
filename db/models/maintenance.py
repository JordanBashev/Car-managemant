from datetime import date
from sqlmodel import Field, Relationship, SQLModel

from .cars import Car
from .garage import Garage

class Maintenance(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    serviceType: str = Field(index=True)
    scheduledDate: date | None

    carId: int = Field(foreign_key="car.id", nullable=False)
    garageId: int = Field(foreign_key="garage.id", nullable=False)

    cars: Car | None = Relationship(back_populates="maintenances")
    garages: Garage | None = Relationship(back_populates="maintenances")