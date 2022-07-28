import requests
import os
from bs4 import BeautifulSoup
import csv
import datetime


start_time = datetime.datetime.now()

url = 'https://ремонт-рулевых-реек.рф/price'

headers = {
    "Accept": "text/css,*/*;q=0.1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36"
}


def get_data():
    req = requests.get(url=url, headers=headers)
    req.encoding = 'UTF8'
    src = req.text

    with open('ремонт_рулевых_реек.html', 'w', encoding='utf-8') as file:
        file.write(src)


# Парсим все нужные категории
    dict_categories = []

    with open('ремонт_рулевых_реек.html', 'r', encoding='utf-8') as file:
        src1 = file.read()

    soup1 = BeautifulSoup(src1, 'lxml')

    item = soup1.find('ul', class_='item-list-price-main-ul').find_all('li')
    count = 0
    for x in item:
        count += 1
        name_categories = x.find('span').find('a').text
        a_href = 'https://ремонт-рулевых-реек.рф' + x.find('span').find('a').get("href")
        img_logo = x.find('div', class_='field-content').find('img').get('src')

        req = requests.get(url=a_href, headers=headers)
        src2 = req.text


# Создаём папку Все_каталоги_реек
        if not os.path.exists('Все_каталоги_реек'):
            os.mkdir('Все_каталоги_реек')

        with open(f'Все_каталоги_реек\{count}.html', 'w', encoding='utf-8') as file:
            file.write(src2)

        with open(f'Все_каталоги_реек\{count}.html', 'r', encoding='utf-8') as file:
            src3 = file.read()

        soup2 = BeautifulSoup(src3, 'lxml')
        CAR_MODEL = soup2.find('table', class_='views-table cols-4 table').find('tbody').find_all('tr')
        count1 = 0
        for x1 in CAR_MODEL:
            count1 += 1
            car_model = x1.find('td', class_='views-field views-field-name-1 views-align-center').find('a').text
            car_model_href = 'https://ремонт-рулевых-реек.рф' + x1.find('td', class_='views-field views-field-name-1 views-align-center').find('a').get('href')
            img_car = str(x1.find(class_='views-field views-field-field-foto-all-care views-align-center').find('img').get('src'))
            img_car_new = img_car.replace('thumbnail', 'large')
            spare_parts_repairs = x1.find(class_='views-field views-field-field-price-fix views-align-center').find('a').text
            removal_installation = x1.find(class_='views-field views-field-field-price-install views-align-center').find('a').text


# Добавление всех
            dict_categories.append(
                {
                    "Название категория": name_categories,
                    "Ссылка на фото категории": img_logo,
                    "Ссылка на страницу категории": a_href,
                    "Название элемента": car_model,
                    "Ссылка на фото элемента": img_car_new,
                    "Запчасти и ремонт": spare_parts_repairs,
                    "Снятие и установка": removal_installation,
                    "Ссылка на элемент": car_model_href
                }
            )


# Создаём csv файл
            with open("categories.csv", 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        "Название категория",
                        "Ссылка на фото категории",
                        "Ссылка на страницу категории",
                        "Название элемента",
                        "Ссылка на фото элемента",
                        "Запчасти и ремонт",
                        "Снятие и установка",
                        "Ссылка на элемент"
                    )
                )

            for x2 in dict_categories:
                with open("categories.csv", 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            x2["Название категория"],
                            x2["Ссылка на фото категории"],
                            x2["Ссылка на страницу категории"],
                            x2["Название элемента"],
                            x2["Ссылка на фото элемента"],
                            x2["Запчасти и ремонт"],
                            x2["Снятие и установка"],
                            x2["Ссылка на элемент"]
                        )
                    )


def main():
    get_data()

# Секундомер
    finish_time = datetime.datetime.now()
    spent_time = finish_time - start_time
    print(spent_time)

if __name__ == '__main__':
    main()
