from bs4 import BeautifulSoup
from database import get_data
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

data = get_data()
site_prices = {}

if data:
    for title, url, xpath in data:
        if title == 'Пусто' or url == 'Пусто' or xpath == 'Пусто':
            continue
        request = requests.get(url, headers=headers)
        if 'text/html' in request.headers.get('content-type', ''):
            match = re.match(r"//(\w+)\[@class=['\"]([^'\"]+)['\"]\]", xpath)

            if match:
                x1, y1 = match.groups()

            soup = BeautifulSoup(request.text, "html.parser")
            check = soup.find_all(x1, class_=y1)

            prices = []
            for item in check:
                price_text = item.get_text()
                price_clean = re.sub(r'[^0-9.,]', '', price_text).replace(',', '.')

                try:
                    price_value = float(price_clean)
                    prices.append(price_value)
                except ValueError:
                    continue

            if prices:
                avg_price = sum(prices) / len(prices)
                site_prices[url] = avg_price
                print(f"Средняя цена на {url}: {avg_price:.2f}")

    overall_avg_price = sum(site_prices.values()) / len(site_prices) if site_prices else 0
    print(f"Общая средняя цена: {overall_avg_price:.2f}")
else:
    raise ValueError("Нет нужной переменной")
