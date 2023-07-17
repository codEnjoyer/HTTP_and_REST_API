from datetime import timedelta

from timeloop import Timeloop
from urllib3.util import Url
import requests as req
from random import choice

from parser.tasks import scrape_faberlic
from src.schemas import FaberlicLanguages

timeloop = Timeloop()
logger = timeloop.logger
logger.name = "sender"


@timeloop.job(interval=timedelta(seconds=60), initial_delay=timedelta(seconds=10))
def send_prices() -> None:
    logger.info("Started to send prices")
    url = Url(scheme="https", host="faberlic.com", path="/index.php")
    idcategory_range = [1001159186333, 1001159186342, 1001159219927, 1001159219928, 1001159219901, 1001159219907,
                        1001159219914, 1001159219921, 1000175334795, 1000180022520, 1000195948255, 1000175334843,
                        1000180022517, 1000180022518]
    params3 = {"option": "com_catalog",
               "view": "listgoods",
               "idcategory": choice(idcategory_range),
               "Itemid": 2075,
               "lang": FaberlicLanguages.RU}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,",
        "cookie": """idorgunit=1000034210371; __session_count_setuped=1; __session_count_total=1; _ga=GA1.2.519736212.1689503193; _gid=GA1.2.34823027.1689503193; uxs_uid=3c754fa0-23c3-11ee-af57-b37908df8de8; uem_user_id="0e6ec2ae-b3b1-4e93-b581-405921c6da1c"; _ym_uid=1689503196239255088; _ym_d=1689503196; tmr_lvid=40a1e9f48296bc92c7c1935d39e47852; tmr_lvidTS=1689503326659; jfcookie[lang]=ru; 2b197b5bc5cb74f1f9938dac62e78e61=m9emd8rn6gl0en4ql2p9q3bik2; utmdata=[]; n9eb05770faf6237e07cf1b90236b87fe=1; QueueITAccepted-SDFrts345E-V3_faberliccom=EventId=faberliccom&QueueId=18d8b465-62b3-4f2b-8863-f50ae854a8db&RedirectType=safetynet&IssueTime=1689599463&Hash=bcc98acfe48c68a9187acb51819e03d7adabe7b95b08f0ef2d04268ff7aed296; wrUserId=19:920f9975-30da-450d-b3ad-fc63fb9dcd92; _ym_isad=1; _ym_visorc=b; tmr_detect=1|1689600363264; gssc213097=; lastUpdate=1689600998000; __zzatgib-w-faberlic-o=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VmRCJaG08jXUkUEXlaVxVALyUXEExeb3owdRs3V10cESRYDiE/C2lbVjRnFRtASBgvS255MURrHWBHWR9DXFZ1F2BKQys2FkZGHHIzdz9rCCIZURMqX3hHV2tlVUI4MWcMT09NEhY=amXSYw==; country=RU; cfidsgib-w-faberlic-o=AurrSyno+T1jy2UquWpKEC8rXSZtUPrLWa4Cft8xjp4qZGtCR+O7rIzxg68QSmCnzDQBpc+eEZOxfI9tO1Zi/l08bmkGqz47iafgwyTpAqfXpUngnbevHuk9qr2gujk/dUQaeDa0rfuAV6ymwuaBmIK4C9Tz84soFebWMak=; session-cookie=1772ab28ad6aa49469428fc1beb261f59c1fa6d5091b46561e1dfc213a003cdef5794fa0bcf0c434926d96045630e240; cfidsgib-w-faberlic-o=AurrSyno+T1jy2UquWpKEC8rXSZtUPrLWa4Cft8xjp4qZGtCR+O7rIzxg68QSmCnzDQBpc+eEZOxfI9tO1Zi/l08bmkGqz47iafgwyTpAqfXpUngnbevHuk9qr2gujk/dUQaeDa0rfuAV6ymwuaBmIK4C9Tz84soFebWMak=; gsscgib-w-faberlic-o=/GSSYlXyxNtwETt8dR7vuUHVKaNAOujfPJC9b4OA+jrRPofEMJkoSWi9Ccmf74rtA1RugREMOhjYnBF1rmx00sYGly9q8ujJyzJCQafVVxSs9vtlY59tXlQlbBk5RxuGXU4coLQnHIAtgeZc1sYp20E4Ss/AfrG3M/Kn/YSSr3YB+OIO7sMJReKpoBi6EAeNaKSI5dW+/N2D+i8cHrkUxsoBN8qUOidOZo8XmcjRKNCSaLG3/+8rx45yeK4VufLYTzaaHbWqZoH3HH9f5hSmZTT00zGq4aAODgzWq/QFYa65Y518NoLKW3XW; _gat_UA-24969553-2=1; fgsscgib-w-faberlic-o=i9XQ9dc8f4b535fdd822bc39a93b85334b5cae74; RT="z=1&dm=faberlic.com&si=bb8b31ec-de90-46e5-8b21-ef5fb6cbd69d&ss=lk6vw21t&sl=i&tt=1d2b&bcn=https://uem.faberlic.com/uem/beacon&obo=2&nu=814e907a211112985e3ff71d3db9973a&cl=x6oi&ld=x6ov&r=7f5069717d1c38a1d79351a292480cc5&ul=x6ox""",
    }
    logger.info(f"Started to scrape prices with this params: %s" % params3)
    prices = scrape_faberlic(url=url, params=params3, headers=headers)
    if not prices:
        logger.info("Prices wasn't found. We'll repeat scraping after a minute.")
        return
    logger.info("Finished to scrape prices")
    for price in prices:
        logger.info(f"Sending price %s" % price.model_dump())
        resp = req.post(url="http://localhost:8000/prices", json=price.model_dump())
        logger.info("Status code: %s, details: %s" % (resp.status_code, resp.text))
    logger.info("Finished to send prices. We'll repeat scraping after a minute.")
