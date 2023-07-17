import datetime

from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PriceCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=512, default="Default")
    price: float = Field(ge=0, default=0)

    def __str__(self):
        return f"({self.name}, {self.price} руб)"


class PriceRead(PriceCreate):
    id: PositiveInt
    published_at: datetime.datetime


class PriceUpdate(BaseSchema):
    name: str | None = Field(min_length=1, max_length=512, default=None)
    price: float | None = Field(ge=0, default=None)
