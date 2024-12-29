from datetime import date
from sqlmodel import Field, SQLModel


class Garage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str = Field(index=True)
    city: str = Field(index=True)
    capacity: int = Field(index=True, default=0)

    start_date: date | None
    end_date:date | None