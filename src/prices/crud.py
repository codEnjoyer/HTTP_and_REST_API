from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Price
from .schemas import PriceCreate, PriceUpdate


def get_all_prices(db: Session) -> list[type[Price]]:
    return db.query(Price).all()


def get_price_by_id(db: Session, id: int) -> type[Price] | None:
    result = db.query(Price).filter(Price.id == id).first()
    return result if result else None


def get_price_by_name(db: Session, name: str) -> type[Price] | None:
    result = db.query(Price).filter(Price.name == name).first()
    return result if result else None


def get_prices_by_names(db: Session, names: list[str]) -> list[type[Price]]:
    return db.query(Price).filter(Price.name.in_(names)).all()


def create_price(db: Session, item: PriceCreate) -> Price | None:
    same_name_existing_items = get_prices_by_names(db, [item.name])
    if same_name_existing_items and item.price in [existing_item.price for existing_item in same_name_existing_items]:
        return None
    db_item = Price(**item.model_dump())
    db.add(db_item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    return db_item


def delete_price_by_id(db: Session, id: int) -> type[Price] | None:
    item = get_price_by_id(db, id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item


def put_price_by_id(db: Session, id: int, item: PriceCreate) -> type[Price] | Price:
    db_item = get_price_by_id(db, id)
    if not db_item:
        return create_price(db, item)
    db_item.name = item.name
    db_item.price = item.price
    db.commit()
    db.refresh(db_item)
    return db_item


def patch_price_by_id(db: Session, id: int, item: PriceUpdate) -> type[Price] | None:
    db_item = get_price_by_id(db, id)
    if not db_item:
        return None
    if item.name:
        db_item.name = item.name
    if item.price:
        db_item.price = item.price
    db.commit()
    db.refresh(db_item)
    return db_item
