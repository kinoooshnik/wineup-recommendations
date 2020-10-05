import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
import random

page = 1
max_page = 80
rating = 5
site_id = 7211


def parse_div(div):  # Функция разбора таблицы с вопросом
    res = []
    print("try")
    # these 2 lines to avoid blocking from website
    rand = random.randint(1, 20)
    time.sleep(rand)
    author_and_photo = div.find_all("div", {"class": "authorAndPhoto"})
    product_name = div.find_all("div", {"class": "productName"})
    product_name_link = product_name[0].find("a")
    review_link = "https://irecommend.ru" + product_name_link.get("href")
    # make a request to get a brand of wine
    r = requests.get(
        review_link,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 OPR/71.0.3770.171"
        },
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
    res.append(wine_name)
    res.append(username)
    res.append(user_mark)
    res.append(rating)
    res.append("")
    res.append(brand)
    res.append("")
    res.append(review_link)
    print(res)
    return res


def simple_request():
    with open("irecommend.csv", mode="w", encoding="utf-8") as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
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

    for i in range(9, max_page, 1):
        if i == 0:
            url = "https://irecommend.ru/taxonomy/term/938/reviews?tid=7211"
        else:
            url = "https://irecommend.ru/taxonomy/term/938/reviews?page=%d&tid=%d" % (
                i,
                site_id,
            )  # url страницы
        print(url)
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 OPR/71.0.3770.171"
            },
        )
        print(r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        divs = soup.find_all("div", {"class": "smTeaser plate teaser-item"})

        for div in divs:
            result = parse_div(div)
            wine_name = result[0]
            username = result[1]
            rate = result[2]
            variants_number = result[3]
            wine_type = result[4]
            brand = result[5]
            wine_link = result[6]
            review_link = result[7]
            with open("irecommend.csv", "a", encoding="utf-8") as w_file:
                file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
                file_writer.writerow(
                    [
                        wine_name,
                        username,
                        rate,
                        variants_number,
                        wine_type,
                        brand,
                        wine_link,
                        review_link,
                    ]
                )
            # result.to_csv('irecommend.csv', mode='a', encoding='utf-8', header=False)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    simple_request()
