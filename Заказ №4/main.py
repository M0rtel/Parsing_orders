import os
from selenium import webdriver
from selenium_stealth import stealth # Очень помогает для обхода блокировок на сайтах
from selenium.webdriver.chrome.service import Service # новый вид записи driver
from selenium.webdriver.common.by import By # новый вид записи find_element
from selenium.webdriver.common.action_chains import ActionChains # при ошибке с click помогает!!!
import csv
import datetime
import time


url = 'https://25jul.zetflix-online.net/films/'

def get_data():
    start_time = datetime.datetime.now()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
# Путь для хром бета
    options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
# Сделать в полный экран
    options.add_argument("--start-maximized")
# Отключение Webdriver
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # selenium-stealth
    options.add_experimental_option('useAutomationExtension', False) # selenium-stealth

    try:
        service = Service(executable_path="104.exe")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url=url)

# selenium-stealth
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        actions = ActionChains(driver)
        info_films = []
        page_total = int(driver.find_element(By.XPATH, '//*[@id="bottom-nav"]/div/div/div/a[10]').text)
        for list in range(2, page_total + 1):
            films_page = len(driver.find_elements(By.CLASS_NAME, 'vi-in'))
            for num in range(1, films_page + 1):
                driver.implicitly_wait(5)
                href_film = driver.find_element(By.XPATH,
                                                   f'//*[@id="dle-content"]/div[{num}]/div/a')
                name_film = driver.find_element(By.XPATH, f'//*[@id="dle-content"]/div[{num}]/div/a/div[1]/div').text
                actions.move_to_element(href_film).click().perform()

                driver.implicitly_wait(5)
                time.sleep(0.2)
                rating = driver.find_elements(By.XPATH, '//*[@id="dle-content"]/article/div[1]/div/div[1]/span')
                rating_list = []
                for rating_ in rating:
                    rating_list.append(rating_.text)

                time.sleep(0.2)
                try:
                    year_film = driver.find_element(By.XPATH, '//*[@id="finfo"]/li[1]/span[2]').text
                except:
                    year_film = 'нет'

                time.sleep(0.2)
                try:
                    director = driver.find_element(By.XPATH, '//*[@id="finfo"]/li[4]/span[2]').text
                except:
                    driver = 'нет'

                time.sleep(0.2)
                try:
                    country = driver.find_element(By.XPATH, '//*[@id="finfo"]/li[3]').text[8:]
                except:
                    country = 'нет'

                driver.implicitly_wait(5)
                info_films.append(
                    {
                        'Название фильма': name_film,
                        'Рейтинг': rating_list,
                        'Год выхода': year_film,
                        'Режиссёр': director,
                        'Страна': country
                    }
                )

                driver.back()

            time.sleep(0.25)
            driver.get(f'https://17jul.zetflix-online.net/films/page/{list}/')

    except Exception as ex:
        print(ex)

    finally:
        driver.close() # Выключение окна
        driver.quit() # Выключение chrome

    with open("info_films.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название фильма',
                'Рейтинг',
                'Год выхода',
                'Режиссёр',
                'Страна'
            )
        )

    for x in info_films:
        with open("info_films.csv", 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    x['Название фильма'],
                    x['Рейтинг'],
                    x['Год выхода'],
                    x['Режиссёр'],
                    x['Страна']
                )
            )

# Секундомер
    finish_time = datetime.datetime.now()
    spent_time = finish_time - start_time
    print(spent_time)


def main():
    get_data()


if __name__ == '__main__':
    main()
