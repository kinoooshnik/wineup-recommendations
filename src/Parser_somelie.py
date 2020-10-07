import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm


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

    link = "https://www.somelie.ru"
    wine_link_tr = table.find("a")
    if score_tr != None:
        wine_link = link + wine_link_tr.get("href")

    URL = wine_link
    R = requests.get(URL, headers={"User-Agent": "my-app/0.0.1"})
    SOUP = BeautifulSoup(R.text)
    TABLES = SOUP.find_all("table", {"class": "characteristics"})

    for item in TABLES:
        wine_type_tr = item.find("td")
        if wine_type_tr != None:
            wine_type = wine_type_tr.text
            break

    TABLES = SOUP.find("div", {"class": "subtitle"})
    if TABLES != None:
        brand = TABLES.text

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
    URL = "https://www.somelie.ru/otzyvy/?section=794"
    result = pd.DataFrame()
    R = requests.get(URL, headers={"User-Agent": "my-app/0.0.1"})
    SOUP = BeautifulSoup(R.text)
    TABLE = SOUP.find_all("div", {"class": "news-item"})

    for item in TABLE:
        res = parse_table(item)
        result = result.append(res, ignore_index=True)
    result

    for i in tqdm(range(2, 294)):
        URL = "https://www.somelie.ru/otzyvy/?section=794&PAGEN_3=" + str(i)
        R = requests.get(URL, headers={"User-Agent": "my-app/0.0.1"})
        SOUP = BeautifulSoup(R.text)
        TABLE = SOUP.find_all("div", {"class": "news-item"})
        for item in TABLE:
            res = parse_table(item)
            result = result.append(res, ignore_index=True)
    FILE = "wine.csv"
    result.to_csv(FILE)
