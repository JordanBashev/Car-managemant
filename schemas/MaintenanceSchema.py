from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from datetime import date

from ..db.models.garage import Garage
from ..db.models.cars import Car

class Maintenance(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    serviceType: str
    scheduledDate: date

    carId: int
    garageId: int

    garages: Garage
    cars: Car

class CreateMaintenance(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    serviceType: str
    scheduledDate: date

    garageId: int
    carId: int

class UpdateMaintenance(CreateMaintenance):
    pass