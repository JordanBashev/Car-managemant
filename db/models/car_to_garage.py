from sqlmodel import Field, Relationship, SQLModel

class CarGarageLink(SQLModel, table=True):
    car_id: int = Field(foreign_key="car.id", primary_key=True)
    garage_id: int = Field(foreign_key="garage.id", primary_key=True)