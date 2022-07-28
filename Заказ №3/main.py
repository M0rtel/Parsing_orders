import os
from selenium import webdriver
from selenium_stealth import stealth # Очень помогает для обхода блокировок на сайтах
from selenium.webdriver.chrome.service import Service # новый вид записи driver
from selenium.webdriver.common.by import By # новый вид записи find_element
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains # при ошибке с click помогает!!!
import time
import datetime


url = 'https://b2b.sokolov.ru/catalog/crockery-and-souvenirs'

def get_data():
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
        start_time = datetime.datetime.now()

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

# Вход в ЛК сайта
        time.sleep(1)
        login = driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input')
        login.click()
        login.send_keys('')

        time.sleep(1)
        password = driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[2]/input')
        password.send_keys('')

        time.sleep(1)
        enter = driver.find_element(By.XPATH, '/html/body/div[1]/div/form/button')
        enter.click()
        time.sleep(1)

# Скачиваю html каждого товара!
        actions = ActionChains(driver) # ActionChains
        count = 1

        for num in range(3, 5): # ошибка поэтому на один больше чем надо
            num_all_catalog = driver.find_elements(By.CSS_SELECTOR, 'div[data-q="0"]')
            driver.implicitly_wait(5)

            for click_img_ in num_all_catalog:
                driver.implicitly_wait(5)
                # click_img_.click()
                actions.move_to_element(click_img_).click().perform() # скрины с объяснениями в вк (ActionChains)

                # time.sleep(0.9)
                exc = driver.find_element(By.TAG_NAME, 'body')

                driver.implicitly_wait(5)

# Название и атртикул
                try:
                    title_article = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/span[1]'
                    ).text
                except:
                    title_article = 'нет'

# Цена за штуку
                try:
                    price = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[4]/div/span[2]'
                    ).text
                except:
                    price = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[3]/div/span[2]'
                    ).text

# Вес металла
                try:
                    metal_weight = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[2]/div/div/div[3]/span[2]'
                    ).text
                except:
                    metal_weight = 'нет'

# Вес изделия
                try:
                    product_weight = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[2]/div/div/div[4]/span[2]'
                    ).text
                except:
                    product_weight = 'нет'

# Описание
                try:
                    description = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/span[2]'
                    ).text
                except:
                    description = 'нет'

# Проба /html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[4]/div/span[2]
#       /html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[3]/div/span[2]
                try:
                    test = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[3]/div[1]/div/div[1]/span[2]'
                    ).text
                except:
                    test = 'нет'

# Покрытие
                try:
                    coverage = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[3]/div[1]/div/div[2]/span[2]'
                    ).text
                except:
                    coverage = 'нет'

# Цена за грамм
                try:
                    price_per_gram = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[3]/div[1]/span[2]'
                    ).text
                except:
                    price_per_gram = 'нет'

# Цена по договору подряда
                try:
                    under_the_contract = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[4]/div/span[1]'
                    ).text
                except:
                    under_the_contract = 'нет'

# Вставки
                try:
                    insert = driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div[3]/form/div/div/div[3]/div[3]/div/div[3]/div'
                    ).text
                except:
                    insert = 'нет'

                print(f'{title_article}# {price}# {metal_weight}# {product_weight}# {description}# {test}# {coverage}# {price_per_gram}# {under_the_contract}# {insert}')

                # if not os.path.exists('Посуда_сувениры'):
                #     os.mkdir('Посуда_сувениры')
                #
                # driver.implicitly_wait(10)
                # with open(f'Посуда_сувениры\{count}.html', 'w', encoding='utf-8') as f:
                #     f.write(driver.page_source)

                count += 1

                driver.implicitly_wait(5)
                exc.send_keys(Keys.ESCAPE)

    # Переход на следующую страницу
            driver.get(f'https://b2b.sokolov.ru/catalog/crockery-and-souvenirs?page={num}&per-page=119')
            time.sleep(2.5)

# Секундомер
        finish_time = datetime.datetime.now()
        spent_time = finish_time - start_time
        print(spent_time)

    except Exception as ex:
        print(ex)

    finally:
        driver.close() # Выключение окна
        driver.quit() # Выключение chrome


def main():
    get_data()


if __name__ == '__main__':
    main()
