import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from tqdm import tqdm

MAX_PAGE = 80
RATING = 5
SITE_ID = 7211
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 OPR/71.0.3770.171"
FILE_NAME = "irecommend.csv"


def parse_div(div):  # Функция разбора таблицы с вопросом
    print("try")
    # these 2 lines to avoid blocking from website
    rand = random.randint(1, 20)
    time.sleep(rand)
    author_and_photo = div.find_all("div", {"class": "authorAndPhoto"})
    product_name = div.find_all("div", {"class": "productName"})
    product_name_link = product_name[0].find("a")
    product_name_link_href = product_name_link.get("href")
    review_link = f"https://irecommend.ru{product_name_link_href}"
    # make a request to get a brand of wine
    r = requests.get(
        review_link,
        headers={"User-Agent": USER_AGENT},
    )
    soup = BeautifulSoup(r.text, "html.parser")
    voc_group_vid_37 = soup.find_all("div", {"class": "voc-group vid-37"})
    # print(voc_group_vid_37)
    brand = voc_group_vid_37[0].find("a").text
    print(brand)
    # get wine name
    wine_name = product_name_link.text
    # print(wine_name)
    # print(review_link)
    author_space = author_and_photo[0].find("div", {"class": "authorSpace"})
    half1 = author_space.find_all("div", {"class": "half1"})
    stars_rating = half1[0].find_all("div", {"class": "starsRating"})
    ons = stars_rating[0].find_all("div", {"class": "on"})
    user_mark = 0
    # count user marks
    for on in ons:
        user_mark += 1
    # print(user_mark)
    author_name = half1[0].find("div", {"class": "authorName"})
    # get username
    username = author_name.find("a").text
    # print(username)
    return {
        "wine_name": wine_name,
        "username": username,
        "rating": user_mark,
        "variants_number": RATING,
        "wine_type": "",
        "brand": brand,
        "wine_link": "",
        "review_link": review_link,
    }


def simple_request():
    with open(FILE_NAME, mode="w", encoding="utf-8") as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        file_writer.writerow(
            [
                "wine_name",
                "username",
                "rating",
                "variants_number",
                "wine_type",
                "brand",
                "wine_link",
                "review_link",
            ]
        )
    for i in range(0, MAX_PAGE, 1):
        for j in tqdm(range(0, MAX_PAGE, 1)):
            if i == 0:
                url = f"https://irecommend.ru/taxonomy/term/938/reviews?tid={SITE_ID}"
            else:
                url = f"https://irecommend.ru/taxonomy/term/938/reviews?page={i}&tid={SITE_ID}"  # url страницы
            print(url)
            r = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
            )
            print(r.status_code)
            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", {"class": "smTeaser plate teaser-item"})

            for div in divs:
                result = parse_div(div)
                print(result.values())
                with open(FILE_NAME, "a", encoding="utf-8") as w_file:
                    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
                    file_writer.writerow(result.values())


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    simple_request()
