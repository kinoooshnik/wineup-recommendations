import requests
from bs4 import BeautifulSoup
import time
import random
from tqdm import tqdm
import pandas as pd
import click

MAX_PAGE = 80
RATING = 5
SITE_ID = 7211
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 OPR/71.0.3770.171"
COLUMNS = [
    "wine_name",
    "username",
    "rating",
    "variants_number",
    "wine_type",
    "brand",
    "wine_link",
    "review_link",
]


def parse_div(div):  # Функция разбора таблицы с вопросом
    # these 2 lines to avoid blocking from website
    rand = random.randint(1, 30)
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
    brand = voc_group_vid_37[0].find("a").text
    wine_name = product_name_link.text
    author_space = author_and_photo[0].find("div", {"class": "authorSpace"})
    half1 = author_space.find_all("div", {"class": "half1"})
    stars_rating = half1[0].find_all("div", {"class": "starsRating"})
    ons = stars_rating[0].find_all("div", {"class": "on"})
    user_mark = 0
    # count user marks
    for on in ons:
        user_mark += 1

    author_name = half1[0].find("div", {"class": "authorName"})
    # get username
    username = author_name.find("a").text
    return dict(
        zip(
            COLUMNS,
            [wine_name, username, user_mark, RATING, "", brand, "", review_link],
        )
    )


@click.command()
@click.argument("output_filepath", type=click.Path())
def main(output_filepath):
    if output_filepath.exist():
        df = pd.read_csv(output_filepath)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    for i in tqdm(range(0, MAX_PAGE, 1)):
        if i == 0:
            url = f"https://irecommend.ru/taxonomy/term/938/reviews?tid={SITE_ID}"
        else:
            url = f"https://irecommend.ru/taxonomy/term/938/reviews?page={i}&tid={SITE_ID}"  # url страницы
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        print(r.status_code, url)
        soup = BeautifulSoup(r.text, "html.parser")
        divs = soup.find_all("div", {"class": "smTeaser plate teaser-item"})

        for i, div in enumerate(divs):
            result = parse_div(div)
            print(f"{i} of {len(divs)}", result.values())
            df = df.append(result, ignore_index=True)
            print(len(df.index))
            df.to_csv(output_filepath, index=False)

    # df.to_csv(output_filepath, index=False)


if __name__ == "__main__":
    main()
