import csv
import os
import datetime
import requests
from bs4 import BeautifulSoup


url = 'https://krasnodar.kwt.market/'

headers = {
    "Accept": "text/css,*/*;q=0.1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.4.904 Yowser/2.5 Safari/537.36"
}

def get_data():
# Начало секундомера
    start_time = datetime.datetime.now()

#     req = requests.get(url=url, headers=headers)
#     req.encoding = 'UTF8'
#     src1 = req.text
#
#
# # Сохранение главной страницы
#     # with open('home_page.html', 'w', encoding='utf-8') as file:
#     #     file.write(src)
#
#     with open('home_page.html', 'r', encoding='utf-8') as file:
#         src1 = file.read()
#
#     soup1 = BeautifulSoup(src1, 'lxml')
#
#
# # Парсинг каталогов продукции
#     dict_catalog_and_href = []
#     catalog____ = soup1.find_all('div', class_='bx_catalog_tile')
#     for catalog___ in catalog____:
#         catalog__ = catalog___.find_all('li')
#         for catalog_ in catalog__:
#             catalog = catalog_.find('span', class_='bx_catalog_tile_title h2').find('a').text
#             catalog_href = 'https://krasnodar.kwt.market' + catalog_.find('span', class_='bx_catalog_tile_title h2').find('a').get('href')
#             dict_catalog_and_href.append(
#                 {
#                     catalog[8: -6]: catalog_href
#                 }
#             )
#
#
# # Парсинг каждого каталога
#     all_url_catalogs_and_products = []
#     for href_dict in dict_catalog_and_href[:-6]:
#
#
# # Парсинг ссылки продуктов с первой страници каталогов
#         for catalog_new, href in href_dict.items():
#             req = requests.get(url=href, headers=headers)
#             req.encoding = 'UTF8'
#             src2 = req.text
#
#             # if not os.path.exists('Каталоги'):
#             #     os.mkdir('Каталоги')
#             #
#             # if not os.path.exists(f'Каталоги\{catalog_new}'):
#             #     os.mkdir(f'Каталоги\{catalog_new}')
#             #
#             # with open(f'Каталоги\{catalog_new}\{catalog_new}.html', 'w', encoding='utf-8') as file:
#             #     file.write(src2)
#
#             with open(f'Каталоги\{catalog_new}\{catalog_new}.html', 'r', encoding='utf-8') as file:
#                 src3 = file.read()
#
#             soup2 = BeautifulSoup(src3, 'lxml')
#             all_href_page = soup2.find('ul', class_='pagination').find_all('li')[-1].find('a').get('href')
#             total_page = int('='.join(all_href_page.split('=')[-1]).replace('=', ''))
#
#             a1 = soup2.find_all('div', class_='main')
#             for i1 in a1:
#                 url_one_page = 'https://krasnodar.kwt.market' + i1.find('a').get('href')
#                 all_url_catalogs_and_products.append(
#                     {
#                         'Название категория': catalog_new,
#                         'Ссылка': url_one_page
#                     }
#                 )
#
#             for page in range(2, total_page + 1):
#                 page_href = f'{href}?PAGEN_1={page}'
#                 req = requests.get(url=page_href, headers=headers)
#                 req.encoding = 'UTF8'
#                 src4 = req.text
#
#                 soup3 = BeautifulSoup(src4, 'lxml')
#
#                 a2 = soup3.find_all('div', class_='main')
#                 for i2 in a2:
#                     url_next_pages = 'https://krasnodar.kwt.market' + i2.find('a').get('href')
#                     all_url_catalogs_and_products.append(
#                         {
#                             'Название категория': catalog_new,
#                             'Ссылка': url_next_pages
#                         }
#                     )
#
# # Сохранение всех ссылок и каталогов в csv
#     with open("categories.csv", 'w', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(
#             (
#                 "Название категория",
#                 "Ссылка"
#             )
#         )
#
#
#     for x1 in all_url_catalogs_and_products:
#         with open("categories.csv", 'a', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(
#                 (
#                     x1["Название категория"],
#                     x1["Ссылка"]
#                 )
#             )


# Экспорт данных из csv в список со словарями
    all_url_catalogs_and_products = []
    with open("categories.csv", 'r', encoding='utf-8') as file:
        data_reader = csv.reader(file)
        for line in data_reader:
            if len(line) == 2:
                if line[0] == 'Название категория':
                    continue
                all_url_catalogs_and_products.append(
                    {
                        line[0]: line[1]
                    }
                )


# Начало парсинга каждого товара
    count = 0
    count_all = len(all_url_catalogs_and_products)
    for all_url_catalog_and_product in all_url_catalogs_and_products:
        for catalog_file, url_page in all_url_catalog_and_product.items():
            req = requests.get(url=url_page, headers=headers)
            req.encoding = 'UTF8'
            src5 = req.text

            count += 1

            if not os.path.exists(f'Каталоги\{catalog_file}\Товары'):
                os.mkdir(f'Каталоги\{catalog_file}\Товары')

            with open(f'Каталоги\{catalog_file}\Товары\{count}.html', 'w', encoding='utf-8') as file:
                file.write(src5)

            with open(f'Каталоги\{catalog_file}\Товары\{count}.html', 'r', encoding='utf-8') as file:
                src6 = file.read()

            soup4 = BeautifulSoup(src6, 'lxml')
            title = soup4.find('h1', class_='title-tovar').text
            way = ''.join(f"{soup4.find('ol', class_='breadcrumb').find_all('li')[1].text[7:-6]}/{soup4.find('ol', class_='breadcrumb').find_all('li')[2].text[8:-6]}".split())
            price = ''.join(soup4.find('p', class_='price').text.split())

            country = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[0].find_all('td')[1].text.split())
            manufacturer = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[1].find_all('td')[1].text.split())
            main_power = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[2].find_all('td')[1].text.split())
            max_power = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[3].find_all('td')[1].text.split())
            voltage = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[4].find_all('td')[1].text.split())
            launch_type = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[5].find_all('td')[1].text.split())
            current_frequency = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[6].find_all('td')[1].text.split())
            inverter_model = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[7].find_all('td')[1].text.split())
            welding_function = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[8].find_all('td')[1].text.split())
            availability_of_autorun = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[9].find_all('td')[1].text.split())
            execution = ' '.join(soup4.find('table', class_='table-striped table-set').find_all('tr')[10].find_all('td')[1].text.split())

            print(country, manufacturer, main_power, max_power, voltage, launch_type, current_frequency, inverter_model,
                  welding_function, availability_of_autorun, execution)


            print(f'{count} из {count_all}')

# Конец секундомера
    finish_time = datetime.datetime.now()
    spent_time = finish_time - start_time
    print(spent_time)


def main():
    get_data()


if __name__ == "__main__":
    main()
