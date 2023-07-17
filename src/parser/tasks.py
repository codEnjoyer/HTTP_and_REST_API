from urllib3.util import Url

from prices.schemas import PriceCreate

import requests as req
from bs4 import BeautifulSoup


def parse_price(raw_price: str) -> float:
    return float(raw_price.split(" ")[0])


def get_prices_from_page(html: str) -> list[PriceCreate] | None:
    bs = BeautifulSoup(html, "lxml")
    catalog = bs.find("div", class_="catalogBody")
    if not catalog:
        return None
    items = catalog.find_all("a", class_="card")
    if not items:
        return None
    prices = []
    for item in items:
        name = item.find("h3", class_="cardTitle").text
        raw_price = item.find("p", class_="cardPriceSale").text
        price = parse_price(raw_price)
        prices.append(PriceCreate(name=name, price=price))
    return prices


def scrape_faberlic(url: Url, params: dict[str, str | int], headers: dict[str, str]) -> list[PriceCreate] | None:
    response = None
    try:
        response = req.get(url=url, params=params, headers=headers)
    except Exception as exc:
        print(exc)
        return None
    prices = get_prices_from_page(response.text)
    return prices if prices else []


def main():
    url = Url(scheme="https", host="faberlic.com", path="/index.php")
    params3 = {"option": "com_catalog", "view": "listgoods", "idcategory": 1000175334844, "Itemid": 2075,
               "lang": "ru"}
    prices = scrape_faberlic(url, params=params3)
    print(prices)


if __name__ == "__main__":
    main()
