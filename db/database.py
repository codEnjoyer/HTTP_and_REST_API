from typing import Iterable
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement

from sqlalchemy import create_engine, Integer, String, MetaData, select, Float, delete
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

metadata = MetaData()
Base = declarative_base(metadata=metadata)

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


class Card(Base):
    __tablename__ = "card"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=512), nullable=False, default="None", unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    def __str__(self):
        return f"{self.name} {self.price}"


def create_table(name: str) -> Session:
    table_name = name.lower()
    engine = create_engine(f"sqlite:///{table_name}.sqlite")
    metadata.create_all(bind=engine)
    logger.info(f"Создана сессия к таблице '{table_name}'")
    return Session(bind=engine)


def clear_table(session: Session, table: type[Base]) -> None:
    stmt = delete(table)
    session.execute(stmt)
    session.commit()
    logger.info(f"Таблица '{table.__tablename__}' была очищена")


def fill_with_data(session: Session, data: Iterable[tuple[str, float]]) -> None:
    for name, price in data:
        item = Card(name=name, price=price)
        try:
            session.add(item)
            session.commit()
            logger.info(f"Предмет '{item}' был добавлен")
        except IntegrityError as err:
            logger.error(f"Не удалось добавить '{item.name}' из-за существующей записи '{err.params[0]}'")
            session.rollback()
    logger.info("Все предметы были обработаны")


def print_all_data(session: Session, table: type[Base]) -> None:
    data = session.execute(select(table)).scalars()
    for item in data:
        print(item)


def parse_price(raw_price: str) -> float:
    price = raw_price[:-1].replace(" ", "")
    return float(price)


def parse_cards(cards: Iterable[WebElement]) -> Iterable[tuple[str, float]]:
    def _parse_card(card: WebElement) -> tuple[str, float]:
        title = card.find_element(By.CLASS_NAME, "indexGoods__item__name").text
        raw_price = card.find_element(By.CLASS_NAME, "price").text
        price = parse_price(raw_price)
        return title, price

    return tuple(map(lambda card: _parse_card(card), cards))


def get_data_from_online(url: str) -> Iterable[tuple[str, float]]:
    with webdriver.Chrome() as driver:
        driver.get(url=url)
        logger.info(f"Идёт получение страницы по адресу '{url}'")
        content_grid = WebDriverWait(driver, timeout=.5) \
            .until(
            EC.presence_of_element_located(
                (By.XPATH, """//div[@class="goods__items  minilisting  borderedTiles js__goods__items"]""")))
        laptop_cards: list[WebElement] = content_grid.find_elements(By.CLASS_NAME, "indexGoods__item")
        logger.info("Получен список карточек, идёт парсинг")
        return parse_cards(laptop_cards)


def main():
    session = create_table("Card")
    # clear_table(session, Card)
    data = get_data_from_online("https://onlinetrade.ru/catalogue/noutbuki-c9/")
    fill_with_data(session, data)


if __name__ == "__main__":
    main()
