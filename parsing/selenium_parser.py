from typing import Dict, List
from selenium import webdriver
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.ozon.ru/product/harakteristiki-konstruktor-lego-super-heroes-novyy-asgard-bro-tora-76200" \
              "-859801694/?asb2=B8PRssGyAeoWU8jpF_ZTebYXhw3hqIxWADUfVDZXbaZGofw7zcLjGPLhZTrWBHQn&avtc=1&avte=2&avts" \
              "=1688657443&keywords=%D0%9A%D0%BE%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D0%BE%D1%80+LEGO&sh" \
              "=G9o2ckYwYg"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 "
                  "Safari/537.36",
    "Cookie": "__exponea_etc__=a0abaedc-b297-434a-94bc-a492a53ae12a; "
              "__Secure-ext_xcid=03e03cdbe57fe479de2226e6561903ce; __Secure-ab-group=34; __Secure-user-id=118532884; "
              "__Secure-access-token=3.118532884.PH_gUaO_R5Wju56V_SY3gw.34.l8cMBQAAAABkpt3"
              "-AAAAAKN3ZWKrNzkxMjIwODAwNDUAgJCg.20221025192119.20230706173006.c67gl9cT42pI9AXZk"
              "-w1Q6zQMkE4clp6VbvnxvrmO4o; "
              "__Secure-refresh-token=3.118532884.PH_gUaO_R5Wju56V_SY3gw.34.l8cMBQAAAABkpt3"
              "-AAAAAKN3ZWKrNzkxMjIwODAwNDUAgJCg.20221025192119.20230706173006"
              ".nceJDTeYt5TYdBOs1wQfeXbC9vagprHN98kykAXViHo; xcid=30b9ad72ea0a999ad296d42847ab134c; "
              "__cf_bm=.JeAwoQ16Eep8uOxM11QsBL5I2jfhlWYor1BelcmxO0-1688657408-0"
              "-AXNFqXSz5hBBAguCqnxMqq59KVQrtXVBHibLAudYxu9UIDhOGSN6J3YFrmX0uvrIwWAJJynqzUmneSocpyIDQat4T6vKA5FDLsv9DYZRrUuj; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwtMSwtMSwtMTYyOTc1NTg0NyxXM3NpYm1GdFpTSTZJbEJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFsSUZCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxcGRXMGdVRVJHSUZacFpYZGxjaUlzSW1SbGMyTnlhWEIwYVc5dUlqb2lVRzl5ZEdGaWJHVWdSRzlqZFcxbGJuUWdSbTl5YldGMElpd2liV2x0WlZSNWNHVnpJanBiZXlKMGVYQmxJam9pWVhCd2JHbGpZWFJwYjI0dmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmU3g3SW5SNWNHVWlPaUowWlhoMEwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjFkZlN4N0ltNWhiV1VpT2lKTmFXTnliM052Wm5RZ1JXUm5aU0JRUkVZZ1ZtbGxkMlZ5SWl3aVpHVnpZM0pwY0hScGIyNGlPaUpRYjNKMFlXSnNaU0JFYjJOMWJXVnVkQ0JHYjNKdFlYUWlMQ0p0YVcxbFZIbHdaWE1pT2x0N0luUjVjR1VpT2lKaGNIQnNhV05oZEdsdmJpOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5TEhzaWRIbHdaU0k2SW5SbGVIUXZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlYxOUxIc2libUZ0WlNJNklsZGxZa3RwZENCaWRXbHNkQzFwYmlCUVJFWWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDFkLFd5SnlkUzFTVlNKZCwwLDEsMCwyNCwyMzc0MTU5MzAsOCwyMjcxMjY1MjAsMSwxLDAsLTQ5MTI3NTUyMyxSMjl2WjJ4bElFbHVZeTRnVG1WMGMyTmhjR1VnUjJWamEyOGdWMmx1TXpJZ05TNHdJQ2hYYVc1a2IzZHpJRTVVSURFd0xqQTdJRmRwYmpZME95QjROalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE1Ea3VNQzR3TGpBZ1UyRm1ZWEpwTHpVek55NHpOaUF5TURBek1ERXdOeUJOYjNwcGJHeGgsZXlKamFISnZiV1VpT25zaVlYQndJanA3SW1selNXNXpkR0ZzYkdWa0lqcG1ZV3h6WlN3aVNXNXpkR0ZzYkZOMFlYUmxJanA3SWtSSlUwRkNURVZFSWpvaVpHbHpZV0pzWldRaUxDSkpUbE5VUVV4TVJVUWlPaUpwYm5OMFlXeHNaV1FpTENKT1QxUmZTVTVUVkVGTVRFVkVJam9pYm05MFgybHVjM1JoYkd4bFpDSjlMQ0pTZFc1dWFXNW5VM1JoZEdVaU9uc2lRMEZPVGs5VVgxSlZUaUk2SW1OaGJtNXZkRjl5ZFc0aUxDSlNSVUZFV1Y5VVQxOVNWVTRpT2lKeVpXRmtlVjkwYjE5eWRXNGlMQ0pTVlU1T1NVNUhJam9pY25WdWJtbHVaeUo5ZlgxOSw2NSw1MjEwNTE5MTEsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4NywxMTY0MjQ2OTU5LDg=; ADDRESSBOOKBAR_WEB_CLARIFICATION=1688657409; is_cookies_accepted=1",
}


def get_general_info(html: str | bytes, to_find: Dict[str, str | Dict[str, str]]) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    findings = []
    for name, attr in to_find.items():
        elem = soup.find(name, attr).get_text()
        findings.append(elem)
    return findings


def main():
    with webdriver.Chrome() as driver:
        driver.get(url=PRODUCT_URL)
        to_find = {"h1": {"class": "z8k"},
                   "span": {"class": "kz5"}}
        info = get_general_info(driver.page_source, to_find)
        print("\n".join(info))


if __name__ == "__main__":
    main()
