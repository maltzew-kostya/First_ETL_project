#Стандартные библиотеки
import os
import csv
import logging
from pathlib import Path
from datetime import datetime
from decimal import Decimal
#Сторонние библиотеки
import psycopg
from dotenv import load_dotenv


#Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    filename = 'etl.log',
    encoding='UTF-8'
)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('ETL pipeline запущен')

#Загрузка переменных окружения - поиск файла .env
load_dotenv()

#Прописываем пути к файлам
BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / 'data' / 'processed' / 'users_clean.csv'
ORDERS_FILE = BASE_DIR / 'data' / 'processed' / 'orders_clean.csv'

try:
    with psycopg.connect(
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT'),
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    ) as conn:
        logger.info('Подключение к БД выполнено')
        with conn.cursor() as cur:
            with (
                open(USERS_FILE, 'r', encoding='utf-8') as f_u,
                open(ORDERS_FILE, 'r', encoding='utf-8') as f_o
            ):
                logger.info('Начало загрузки пользователей')
                users_count = 0
                for row in csv.DictReader(f_u):
                    age = int(row['age']) if row['age'] else None
                    if row['registered_at']:
                        registered_at = datetime.strptime(row['registered_at'], '%Y-%m-%d %H:%M:%S')
                    else:
                        registered_at = None
                    value = (
                        int(row['user_id']),
                        row['name'],
                        row['city'],
                        age,
                        row['source'],
                        registered_at
                    )
                    cur.execute(
                        '''
                        INSERT INTO users (user_id, name, city, age, source, registered_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''',
                        value
                    )
                    users_count += 1
                logger.info(f'Данные пользователей успешно загружены: {users_count} записей')

                logger.info('Начало загрузки заказов')
                orders_count = 0
                for row in csv.DictReader(f_o):
                    amount = Decimal(row['amount']) if row['amount'] else None
                    if row['order_date']:
                        order_date = datetime.strptime(row['order_date'], '%Y-%m-%d %H:%M:%S')
                    else:
                        order_date = None
                    value = (
                        int(row['order_id']),
                        int(row['user_id']),
                        order_date,
                        row['category'],
                        amount,
                        row['status']
                    )
                    cur.execute(
                        '''
                        INSERT INTO orders (order_id, user_id, order_date, category, amount, status)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''',
                        value
                    )
                    orders_count += 1
                logger.info(f'Данные заказов успешно загружены: {orders_count} записей')
    logger.info('ETL pipeline успешно завершен')
except psycopg.OperationalError:
    logger.exception('Ошибка подключения к БД')
    raise
except psycopg.Error:
    logger.exception('Ошибка PostgreSQL во время загрузки данных')
    raise
except FileNotFoundError:
    logger.exception('Не найден CSV файл')
    raise
except (ValueError, KeyError):
    logger.exception('Ошибка преобразования данных при загрузке')
    raise
except Exception:
    logger.exception('Непредвиденная ошибка ETL pipeline')
    raise


