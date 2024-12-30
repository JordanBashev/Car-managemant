from datetime import date
from sqlmodel import Field, Relationship, SQLModel

from .car_to_garage import CarGarageLink


class Garage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str = Field(index=True)
    city: str = Field(index=True)
    capacity: int = Field(index=True, default=0)

    start_date: date | None
    end_date: date | None

    cars: list["Car"] = Relationship(back_populates="garages", link_model=CarGarageLink) # type: ignore
    maintenances: list["Maintenance"] = Relationship(back_populates="garages") # type: ignore