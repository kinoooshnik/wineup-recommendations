import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm

MIN_PAGE = 2
MAX_PAGE = 295
MY_APP = "my-app/0.0.1"
LINK = "https://www.somelie.ru"
FILE_NAME = "wine.csv"


def parse_table(table):
    res = pd.DataFrame()
    wine_name = ""
    username = ""
    wine_type = ""
    brand = ""
    wine_link = ""
    review_link = ""

    name_tr = table.find("b")
    if name_tr != None:
        wine_name = name_tr.text.strip()

    login_tr = table.find("small")
    if login_tr != None:
        username = login_tr.text.strip()

    score_tr = table.find("div", {"class": "rating"}).find("a")
    if score_tr != None:
        rating = score_tr.text.strip()

    wine_link_tr = table.find("a")
    if score_tr != None:
        wine_link = LINK + wine_link_tr.get("href")
    url = wine_link
    r = requests.get(url, headers={"User-Agent": MY_APP})
    soup = BeautifulSoup(r.text)
    tables = soup.find_all("table", {"class": "characteristics"})

    for item in tables:
        wine_type_tr = item.find("td")
        if wine_type_tr != None:
            wine_type = wine_type_tr.text
            break

    tables = soup.find("div", {"class": "subtitle"})
    if tables != None:
        brand = tables.text

    variants_number = 5
    time.sleep(3)
    res = res.append(
        pd.DataFrame(
            [
                [
                    wine_name,
                    username,
                    rating,
                    variants_number,
                    wine_type,
                    brand,
                    wine_link,
                    review_link,
                ]
            ],
            columns=[
                "wine_name",
                "username",
                "rating",
                "variants_number",
                "wine_type",
                "brand",
                "wine_link",
                "review_link",
            ],
        ),
        ignore_index=True,
    )
    return res


def main():
    url = "https://www.somelie.ru/otzyvy/?section=794"
    result = pd.DataFrame()
    r = requests.get(url, headers={"User-Agent": MY_APP})
    soup = BeautifulSoup(r.text)
    table = soup.find_all("div", {"class": "news-item"})

    for item in table:
        res = parse_table(item)
        result = result.append(res, ignore_index=True)

    for i in tqdm(range(MIN_PAGE, MAX_PAGE)):
        url = f"https://www.somelie.ru/otzyvy/?section=794&PAGEN_3={i}"
        r = requests.get(url, headers={"User-Agent": MY_APP})
        soup = BeautifulSoup(r.text)
        table = soup.find_all("div", {"class": "news-item"})
        for item in TABLE:
            res = parse_table(item)
            result = result.append(res, ignore_index=True)
    result.to_csv(FILE)

main()
