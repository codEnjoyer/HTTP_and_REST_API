import datetime

from sqlalchemy import Integer, Float, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class Price(Base):
    __tablename__ = "price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=512), nullable=False, default="Default", index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    published_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, default=datetime.datetime.now)

    def __str__(self):
        return f"{self.name} {self.price}"
