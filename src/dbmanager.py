import psycopg2
import json
import os
from config import config, JSON_DATA_DIR


class DBManager:
    """Класс для создания и заполнения БД"""

    def __init__(self):
        self.database_name = None

    @staticmethod
    def db_connection(func):
        """Декоратор для соединения с базой данных
        и закрытия соединения после выполнения запроса"""
        def wrapper(self, *args, **kwargs):
            params = config()
            conn = psycopg2.connect(dbname=self.database_name, **params)
            conn.autocommit = True
            res = func(self, conn, *args, **kwargs)
            conn.close()
            return res

        return wrapper

    @db_connection
    def create_database(self, conn, dbname: str) -> None:
        """
        Метод для создания базы данных
        :param conn: соединение с базой данных
        :param dbname: имя создаваемой базы данных
        """
        try:
            with conn.cursor() as cur:
                cur.execute('DROP DATABASE IF EXISTS {}'.format(dbname))
                cur.execute('CREATE DATABASE {}'.format(dbname))
                self.database_name = dbname
                print(f'База данных {dbname} успешно создана')

        except psycopg2.OperationalError as e:
            print(f'Ошибка создания базы данных: {e}')

    @db_connection
    def create_table(self, conn, db_queries_file: str) -> None:
        """
        Метод для создания таблиц в базе данных
        :param conn: соединение с базой данных
        :param db_queries_file: файл с запросами на создание таблиц в БД
        """
        try:
            with open(db_queries_file, 'r', encoding='utf-8') as file:
                create_table_query = file.read()
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                print(f'Таблицы в базе {self.database_name} успешно созданы')

        except psycopg2.OperationalError as e:
            print(f'Ошибка создания таблицы: {e}')

    @db_connection
    def insert_data_to_table(self, conn, data_filename: str) -> None:
        """
        Метод для заполнения таблиц в базе данных из файла json
        :param conn: соединение с базой данных
        :param data_filename: файл json с данными
        """
        filepath = os.path.join(JSON_DATA_DIR, data_filename)
        with open(filepath, 'r', encoding="utf-8") as file:
            data = json.load(file)

        try:
            with conn.cursor() as cur:
                insert_employers_query = "INSERT INTO employers (employer_name) VALUES (%s)"
                insert_vacancies_query = """INSERT INTO vacancies (
                                            employer_id, vacancy_title, vacancy_url, 
                                            vacancy_area, salary_from, salary_to) 
                                            VALUES (%s, %s, %s, %s, %s, %s)"""
                employers_data = set([(vacancy.get('employer').get('name'),) for vacancy in data])
                cur.executemany(insert_employers_query, employers_data)
                cur.execute("SELECT employer_id, employer_name FROM employers ORDER BY employer_id DESC")
                employers = {row[1]: row[0] for row in cur.fetchall()}
                vacancies_data = []
                for vacancy in data:
                    salary = vacancy.get('salary')
                    if not salary:
                        salary_from = 0
                        salary_to = 0
                    else:
                        salary_from = salary.get('from')
                        salary_to = salary.get('to')
                        if not salary_from:
                            salary_from = salary_to
                        if not salary_to:
                            salary_to = salary_from
                    vacancies_data.append((employers[vacancy.get('employer')['name']], vacancy.get('name'),
                                           vacancy.get('alternate_url'), vacancy.get('area')['name'],
                                           salary_from, salary_to))

                cur.executemany(insert_vacancies_query, vacancies_data)

                print(f'Таблицы успешно заполнены данными из файла {data_filename}')

        except psycopg2.Error as e:
            print(f'Ошибка заполнения таблицы: {e}')
