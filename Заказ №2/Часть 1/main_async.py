import time
import requests
import os
from bs4 import BeautifulSoup
import csv
import datetime
import asyncio
import aiohttp


dict_categories = []
start_time = datetime.datetime.now()


async def get_page_data(session, page):
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36"
    }
    url = f'https://ремонт-рулевых-реек.рф{page}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

        CAR_MODEL = soup.find('table', class_='views-table cols-4 table').find('tbody').find_all('tr')
        count1 = 0
        for x in CAR_MODEL:
            count1 += 1
            car_model = x.find('td', class_='views-field views-field-name-1 views-align-center').find('a').text
            car_model_href = 'https://ремонт-рулевых-реек.рф' + x.find('td', class_='views-field views-field-name-1 views-align-center').find('a').get('href')
            img_car = str(x.find(class_='views-field views-field-field-foto-all-care views-align-center').find('img').get('src'))
            img_car_new = img_car.replace('thumbnail', 'large')
            spare_parts_repairs = x.find(class_='views-field views-field-field-price-fix views-align-center').find('a').text
            removal_installation = x.find(class_='views-field views-field-field-price-install views-align-center').find('a').text

            dict_categories.append(
                {
                    "Название элемента": car_model,
                    "Ссылка на фото элемента": img_car_new,
                    "Запчасти и ремонт": spare_parts_repairs,
                    "Снятие и установка": removal_installation,
                    "Ссылка на элемент": car_model_href
                }
            )


async def gather_data():
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36"
    }

    url = 'https://ремонт-рулевых-реек.рф/price'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        page = len(soup.find('ul', class_='item-list-price-main-ul').find_all('li'))

        tasks = []

        for page_num in range(0, page):
            page = soup.find('ul', class_='item-list-price-main-ul').find_all('li')[page_num].find('a').get('href')
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())

    with open("categories_async.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Название элемента",
                "Ссылка на фото элемента",
                "Запчасти и ремонт",
                "Снятие и установка",
                "Ссылка на элемент"
            )
        )

    for x1 in dict_categories:
        with open("categories_async.csv", 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    x1["Название элемента"],
                    x1["Ссылка на фото элемента"],
                    x1["Запчасти и ремонт"],
                    x1["Снятие и установка"],
                    x1["Ссылка на элемент"]
                )
            )

    finish_time = datetime.datetime.now()
    spent_time = finish_time - start_time
    print(spent_time)


if __name__ == '__main__':
    main()

