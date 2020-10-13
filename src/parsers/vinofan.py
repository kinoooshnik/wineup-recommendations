import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

PAGE = 1
MAX_PAGE = 40
RATING = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 OPR/71.0.3770.171"
FILE_NAME = "vinofan.csv"


def parse_div(div):
    author = div.find_all("div", {"class": "authdate"})
    if div.find_all("div", {"class": "white_link"}):
        product_name = div.find_all("div", {"class": "white_link"})
        color = "white"
    elif div.find_all("div", {"class": "red_link"}):
        product_name = div.find_all("div", {"class": "red_link"})
        color = "red"
    elif div.find_all("div", {"class": "rose_link"}):
        product_name = div.find_all("div", {"class": "rose_link"})
        color = "rose"
    product_name_link = "https://vinofan.ru" + product_name[0].find("a").get("href")
    # make a request to get a brand of wine
    r = requests.get(product_name_link, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(r.text, "html.parser")
    if color == "white":
        header = soup.find_all("div", {"class": "whiteheader"})
    elif color == "red":
        header = soup.find_all("div", {"class": "redheader"})
    elif color == "rose":
        header = soup.find_all("div", {"class": "roseheader"})
    wine_name = header[0].find("h1").text
    username = author[0].find("a").text
    user_mark = (
        div.find_all("div", {"class": "texts_estm"})[0]
        .find_all("img")[1]
        .get("src")
        .split("/")[-1]
        .split("r.jpg")[0]
    )
    wine_type = soup.find_all("div", {"class": "wlist_block"})[1].find("span").text
    brand = soup.find_all("div", {"class": "wlist_block_color"})[0].find("a").text
    wine_link = product_name_link

    return {
        "wine_name": wine_name,
        "username": username,
        "rating": user_mark,
        "variants_number": RATING,
        "wine_type": wine_type,
        "brand": brand,
        "wine_link": wine_link,
        "review_link": "",
    }


def simple_request():
    with open(FILE_NAME, mode="w", encoding="utf-8") as w_file:
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

    for i in tqdm(range(0, MAX_PAGE, 1)):

        url = f"https://www.vinofan.ru/inf/rating/page{i+1}"  # url страницы
        r = requests.get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(r.text, "html.parser")
        divs = soup.find_all("div", {"class": "unitcell"})

        for div in divs:
            result = parse_div(div)
            with open(FILE_NAME, "a", encoding="utf-8") as w_file:
                file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
                file_writer.writerow(result.values())


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    simple_request()
