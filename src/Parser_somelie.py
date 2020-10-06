#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# In[111]:


url = "https://www.somelie.ru/otzyvy/?section=794"
r = requests.get(url, headers={"User-Agent": "my-app/0.0.1"})


# In[112]:


def parse_table(table):  # Функция разбора таблицы с вопросом

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

    url = wine_link
    r = requests.get(url, headers={"User-Agent": "my-app/0.0.1"})
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


# In[113]:


result = pd.DataFrame()

r = requests.get(url)
soup = BeautifulSoup(r.text)  # Отправляем полученную страницу в библиотеку для парсинга
table = soup.find_all("div", {"class": "news-item"})


# In[114]:


for item in table:
    res = parse_table(item)
    result = result.append(res, ignore_index=True)
result


# In[115]:


link = "https://www.somelie.ru/otzyvy/?section=794&PAGEN_3="
for i in range(2, 50):
    url = link + str(i)
    r = requests.get(url, headers={"User-Agent": "my-app/0.0.1"})
    soup = BeautifulSoup(r.text)
    tables = soup.find_all("div", {"class": "news-item"})
    for item in table:
        res = parse_table(item)
        result = result.append(res, ignore_index=True)


# In[163]:


result = result.loc[0:4879, :]
result


# In[165]:


link = "https://www.somelie.ru/otzyvy/?section=794&PAGEN_3="
for i in range(280, 294):
    url = link + str(i)
    r = requests.get(
        url, headers={"User-agent": "Mozilla/5.0", "Referer": "http://www.python.org/"}
    )
    soup = BeautifulSoup(r.text)
    tables = soup.find_all("div", {"class": "news-item"})
    for item in table:
        res = parse_table(item)
        result = result.append(res, ignore_index=True)
result


# In[ ]:


# In[162]:


result


# In[ ]:


# In[ ]:


# In[ ]:


# In[2]:


result.to_csv("wine.csv")


# In[7]:


result = pd.read_csv("wine.csv")
