# -*-coding:utf-8-*-
import pandas as pd

import requests
from bs4 import BeautifulSoup

import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import os
import re

chromedriver = "./chromedriver"
os.environ["webserver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)


def parse_medal_info(html) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html5lib")
    table = soup.findAll("table")[0]
    body = table.findAll("tbody")[0]
    rows = body.findAll("tr")

    medal_df = pd.DataFrame(columns=['country', 'athlete_name', 'sport_name', 'event_name', 'medal_type'])

    for row in rows:
        columns = row.findAll('td')
        country, athlete_name, sport_name, event_name, medal_type = '', '', '', '', ''
        for i in range(len(columns)):
            if i == 0:
                country = columns[i].div.find_all('span', class_="d-none d-md-table-cell")[0].get_text()
            if i == 1:
                athlete_name = columns[i].div.find_all('span', class_="d-none d-md-block")[0].get_text()
            if i == 2:
                sport_name = columns[i].a.get_text().strip()
            if i == 3:
                event_name = columns[i].get_text()
            if i == 4:
                medal_type = columns[i].img.attrs['alt']
        medal_df = medal_df.append(
            {'country': country, 'athlete_name': athlete_name, 'sport_name': sport_name, 'event_name': event_name,
             'medal_type': medal_type}, ignore_index=True)
    return medal_df


if __name__ == '__main__':
    URL = 'https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medalists.htm'

    URL_CN = 'https://olympics.com/tokyo-2020/olympic-games/zh/results/all-sports/medalists.htm'

    browser.get(URL)
    # browser
    result = browser.page_source
    time.sleep(10)
    browser.find_element_by_id(id_="onetrust-accept-btn-handler").click()
    # time.sleep(20)
    result = pd.DataFrame()
    for i in range(121):
        html = browser.page_source
        df = parse_medal_info(html)
        result = result.append(df)
        print(df)
        js = 'var q=document.documentElement.scrollTop=200'
        browser.execute_script(js)
        btn = browser.find_element_by_id(id_='medals-table_next')
        btn.click()
    result.to_csv('./medal_list.csv', encoding='UTF-8')
    browser.close()
