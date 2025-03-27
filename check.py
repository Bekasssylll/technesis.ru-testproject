import time

from bs4 import BeautifulSoup

from database import get_data, delete_data
import requests
import re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

options = Options()
options.add_argument("--headless")  # Запуск без графического интерфейса
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--no-sandbox")

# Правильный способ установки драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

"""
Специально для задачи со звездочкой
Пробегаться по данным и парсить цены
"""
check = []

# delete_data()
# print(get_data())
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}  # Добавляю headers,потому что без него он не запускает на сервер
# print(get_data())
data = get_data()
if data:
    for title, url, xpath in data:
        if title == 'Пусто' or url == 'Пусто' or xpath == 'Пусто':
            continue
        request = requests.get(url, headers=headers)
        # print(request.text)
        if 'text/html' in request.headers.get('content-type', ''):
            match = re.match(r'//(\w+)\[@class="([^"]+)"\]', xpath)
            if match:
                x1, y1 = match.groups()

                # print(f"XPath: {xpath}")
                # print(f"x1 (тег): {x1}, y1 (класс): {y1}")

            soup = BeautifulSoup(request.text, "html.parser")
            check = soup.find_all(x1, class_=y1)
            print(check)
            if not check:
                driver.get(url)
                time.sleep(3)  # Ждём загрузки страницы

                soup = BeautifulSoup(driver.page_source, "html.parser")
                check = soup.find_all(x1, class_=y1)

            print(check)
            print('___________________________________________________________________')

        # print(title, url, xpath)


else:
    raise ValueError("Нет нужной переменной")
