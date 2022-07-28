from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import csv
# import json


headers = {
    "Accept": "text/css,*/*;q=0.1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 Yowser/2.5 Safari/537.36"
}


url = 'https://www.wildberries.ru/catalog/8353036/feedbacks?imtId=6476041&size=28356721'


def get_data():
    count = 0
    options = webdriver.ChromeOptions()
    options.set_capability("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 Yowser/2.5 Safari/537.36")

    options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

    options.add_argument("--start-maximized")

    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service(executable_path="104.exe")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url=url)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        time.sleep(1)

        html = driver.find_element(By.TAG_NAME, "html")

# Парсинг количество отзывов
        count_feedback = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/section/div[1]/div[1]/h1/span').text
        count = int(count_feedback.replace(' ', ''))
        count_scrolling = int(count_feedback.replace(' ', '')) * 2
        time.sleep(1)

        for x in range(count_scrolling):
            html.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        with open("index_selenium.html", "w", encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


    with open("index_selenium.html", 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')


# Парсинг всех отзывов и их рейтинг!!!
    all_comment = soup.find('ul', class_="comments__list").find_all('li')
    star_feedback = []
    star_1_feedback = []
    star_2_feedback = []
    star_3_feedback = []
    star_4_feedback = []
    star_5_feedback = []
    star_all_feedback = [star_1_feedback, star_2_feedback, star_3_feedback, star_4_feedback, star_5_feedback]
    for comment in all_comment:
        star = ''
        for i in range(1, 6):
            if comment.find(class_=f'feedback__rating stars-line star{i}') != None:
                star = f'{i}'
                break

        if comment.find('p') != None: # Проверка, есть ли отзыв с таких путём!!!
            feedback = comment.find('p').text
            star_feedback.append(    # Добавление всех отзывов в список
                {
                    'Star': star,
                    'Feedback': feedback
                }
            )

# Проверка отзыв на звёзды и добавление их в нужный список
            star_int = int(star) - 1
            for x in range(0, 5):
                if star_int == x:
                    star_all_feedback[x].append(feedback)


# Создание csv файла всех отзывов и их рейтинга
    count2 = 0
    with open("feedback_all.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Star',
                'Feedback'
            )
        )

    for x in star_feedback:
        with open("feedback_all.csv", 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    x['Star'],
                    x['Feedback']
                )
            )
        count2 += 1
        print(f'Загружено {count2} из {count}')


# # Создание json файла
#     with open(f"feedback_all.json", "a", encoding='utf-8') as file:
#         json.dump(star_feedback, file, indent=4, ensure_ascii=False)


# Файл с самыми частыми отзывами!
    s = 0
    similar_feedback_1 = []
    similar_feedback_2 = []
    similar_feedback_3 = []
    similar_feedback_4 = []
    similar_feedback_5 = []
    all_similar_feedback = [similar_feedback_1, similar_feedback_2, similar_feedback_3, similar_feedback_4, similar_feedback_5]
    for star_ in star_all_feedback:
        s += 1
        if len(star_) == len(set(star_)):
            print(f'Нет одинаковых комментариев с {s} зв.')

        else:
            print(f'Есть одинаковые комментарии с {s} зв.')
            necessary = all_similar_feedback[s-1]
            for feedback_ in star_:
                if (star_.count(feedback_)) >= 2:
                    necessary.append(
                        {
                            "Star": s,
                            "Count": star_.count(feedback_),
                            "Feedback": feedback_
                        }
                    )


# Создание csv файла с самыми частыми отзывами и их количеством!
    with open("similar_feedback_all.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Star',
                'Count',
                'Feedback'
            )
        )


# Удаление лишних словарей из списка!!
    for x in all_similar_feedback:
        seen = set()
        new_l = []
        for d in x:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)

        for x1 in new_l:
            with open("similar_feedback_all.csv", 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        x1['Star'],
                        x1['Count'],
                        x1['Feedback']
                    )
                )

    print('Парсинг завершён!! Можете закрыть приложение.')


def main():
    get_data()


if __name__ == '__main__':
    main()
