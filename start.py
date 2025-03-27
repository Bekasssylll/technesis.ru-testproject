import asyncio
import logging
import os
import pandas as pd
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import insert_data, get_data

"""
Коротко о start.py:
Телеграмм бот который получает данные(Excel-file)
"""
load_dotenv()
TOKEN = os.getenv('bot_api_key')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Загрузить файл")]],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer("Привет! Загрузите ваш Excel-файл с данными.", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Загрузить файл")
async def request_file(message: types.Message):
    await message.answer("Пришлите Excel-файл в формате .xlsx или .xls.")


if not os.path.exists("downloads"):
    os.makedirs("downloads")


@dp.message(lambda message: message.document)
async def handle_file(message: types.Message):
    document = message.document
    file_name = document.file_name

    if not file_name.endswith((".xlsx", ".xls")):
        await message.answer("Ошибка! Файл должен быть в формате .xlsx или .xls.")
        return

    file_path = f"downloads/{file_name}"
    file = await bot.get_file(document.file_id)
    await bot.download_file(file.file_path, file_path)

    await message.answer("Файл загружен! Обрабатываю...")

    try:
        df = pd.read_excel(file_path)

        if not {'title', 'url', 'xpath'}.issubset(df.columns):
            await message.answer("Ошибка! Файл должен содержать колонки: title, url, xpath.")
            return

        df.fillna("Пусто", inplace=True)

        for _, row in df.iterrows():
            insert_data(row['title'], row['url'], row['xpath'])

        df = df.head(5)

        table_header = f"{'№':<3} | {'Название':<20} | {'Ссылка':<30} | {'XPath':<30}\n" + "-" * 90
        table_rows = [
            f"{index:<3} | {row['title'][:20]:<20} | {row['url'][:30]:<30} | {row['xpath'][:30]:<30}"
            for index, row in df.iterrows()
        ]
        table_text = f"<pre>{table_header}\n" + "\n".join(table_rows) + "</pre>"

        await message.answer(f"Данные из файла:\n{table_text}", parse_mode="HTML")

    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}")


async def main():
    await dp.start_polling(bot)


print(get_data())
if __name__ == "__main__":
    asyncio.run(main())
