from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from .crud import get_all_prices, get_price_by_id, delete_price_by_id, put_price_by_id, patch_price_by_id, create_price
from .schemas import PriceRead, PriceCreate, PriceUpdate

from database import get_session

router = APIRouter(tags=["Prices"], prefix="/prices")


@router.get("", response_model=list[PriceRead], status_code=status.HTTP_200_OK)
def get_prices(db: Annotated[Session, Depends(get_session)]):
    prices = get_all_prices(db)
    return prices


@router.get("/{id}", response_model=PriceRead, status_code=status.HTTP_200_OK)
def get_price(id: int, db: Annotated[Session, Depends(get_session)]):
    price = get_price_by_id(db, id)
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Price not found")
    return price


@router.post("", response_model=PriceCreate,
             status_code=status.HTTP_201_CREATED,
             description="""It takes a list of prices or a single price.""")
def post_price(price: PriceCreate, db: Annotated[Session, Depends(get_session)]):
    result = create_price(db, price)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Price with this name and price already exists")
    return result


@router.delete("/{id}", response_model=PriceRead, status_code=status.HTTP_200_OK)
def delete_price(id: int, db: Annotated[Session, Depends(get_session)]):
    result = delete_price_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return result


@router.put("/{id}", response_model=PriceRead, status_code=status.HTTP_200_OK)
def put_price(id: int, price: PriceCreate, db: Annotated[Session, Depends(get_session)]):
    result = put_price_by_id(db, id, price)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return result


@router.patch("/{id}", response_model=PriceRead, status_code=status.HTTP_200_OK)
def patch_price(id: int, price: PriceUpdate, db: Annotated[Session, Depends(get_session)]):
    result = patch_price_by_id(db, id, price)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return result
