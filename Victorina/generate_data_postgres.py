import psycopg2
from psycopg2 import sql
from string import ascii_letters
from random import shuffle


# Параметры подключения к базе данных
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  # или IP-адрес сервера
    'port': 5432
}


# Данные для вставки
# data_to_insert = [
    # ('John Doe', 28, 'john.doe@example.com'),
    # ('Jane Smith', 34, 'jane.smith@example.com')
# ]
for i in range(10300, 13000):
    # Данные для вставки
    data_to_insert = []
    random_string = [i for i in ascii_letters]
    shuffle(random_string)
    random_string = ''.join(random_string[:10])
    data_to_insert.append([i, random_string])

    # Подключение к базе данных
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # SQL-запрос для вставки данных
        insert_query = sql.SQL("""
            INSERT INTO themes (id, name)
            VALUES (%s, %s)
        """)

        # Вставка данных
        for record in data_to_insert:
            cursor.execute(insert_query, record)

        # Фиксация изменений
        conn.commit()
        print("Данные успешно добавлены!")

    except psycopg2.Error as e:
        print(f"Ошибка при работе с PostgreSQL: {e}")

    finally:
        # Закрытие соединения
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто.")
#
