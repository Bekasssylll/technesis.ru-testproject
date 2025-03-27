import sqlite3

database_name = 'mydatabase.db'


def create_table():
    """Создаёт таблицу, если её нет"""
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                xpath TEXT NOT NULL
            )
        """)
        conn.commit()


def insert_data(title, url, xpath):
    """Добавляет запись в таблицу"""
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)", (title, url, xpath))
        conn.commit()


def get_data():
    """Получает все записи из таблицы"""
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, url, xpath FROM sites")
        rows = cursor.fetchall()
    return rows


def delete_data():
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE from sites")
        conn.commit()


create_table()
