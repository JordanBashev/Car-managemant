from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from datetime import date

class Garage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    city: str
    capacity: int

class CreateGarage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    location: str
    city: str
    capacity: int

class UpdateGarage(CreateGarage):
    pass

class GarageReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    date: date
    requests: int
    availableCapacity: int