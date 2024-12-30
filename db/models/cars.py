from sqlmodel import Field, Relationship, SQLModel

from .car_to_garage import CarGarageLink


class Car(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    make: str = Field(index=True)
    model: str = Field(index=True)
    productionYear: str = Field(index=True)
    licensePlate: str = Field(index=True)

    garages: list["Garage"] = Relationship(back_populates="cars", link_model=CarGarageLink) # type: ignore