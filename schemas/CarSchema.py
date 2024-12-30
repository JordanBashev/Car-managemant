from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from ..db.models.garage import Garage

class Car(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str

    garages: list[Garage]

class CreateCar(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    make: str
    model: str
    productionYear: int
    licensePlate: str

    garageIds: list[int] | None

class UpdateCar(CreateCar):
    pass