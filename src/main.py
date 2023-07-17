from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import engine, get_session

from prices.crud import get_all_prices
from prices.models import Price
from prices.router import router as prices_router
from prices.schemas import PriceRead

from sender.main import timeloop

Price.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    timeloop.start()
    yield
    timeloop.stop()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(prices_router)


@main_app.get("/", tags=["Root"], response_model=list[PriceRead], status_code=status.HTTP_200_OK)
async def root(db: Annotated[Session, Depends(get_session)]):
    return get_all_prices(db)
