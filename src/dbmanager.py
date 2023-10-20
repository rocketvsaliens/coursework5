import psycopg2
import json
import os
from config import config, JSON_DATA_DIR


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self):
        self.database_name = None

    def connect_to_database(self):
        """Метод для подключения к базе данных"""
        params = config()
        return psycopg2.connect(dbname=self.database_name, **params)

    def create_database(self, dbname: str) -> None:
        """
        Метод для создания базы данных
        :param dbname: имя создаваемой базы данных
        """
        try:
            connection = self.connect_to_database()
            connection.autocommit = True
            # Создаём базу данных
            with connection.cursor() as cur:
                cur.execute(f'DROP DATABASE IF EXISTS {dbname}')
                cur.execute(f'CREATE DATABASE {dbname}')
                self.database_name = dbname
                print(f'База данных {dbname} успешно создана')

            connection.close()

        except psycopg2.OperationalError as e:
            print(e)

    def create_table(self, db_queries_file: str) -> None:
        """
        Метод для создания таблиц в базе данных
        :param db_queries_file: файл с запросами на создание таблиц в БД
        """
        try:
            with self.connect_to_database() as connection:
                # Читаем запросы на создание таблиц
                with open(db_queries_file, 'r', encoding='utf-8') as file:
                    create_table_query = file.read()
                # Создаём таблицы
                with connection.cursor() as cur:
                    cur.execute(create_table_query)
                    print('Таблицы успешно созданы')
            connection.commit()
            connection.close()

        except psycopg2.OperationalError as e:
            print(e)

    def insert_data_to_table(self, data_filename: str) -> None:
        """
        Метод для заполнения таблиц в базе данных из файла json
        :param data_filename: файл json с данными
        """
        # Читаем данные из файла
        filepath = os.path.join(JSON_DATA_DIR, data_filename)
        with open(filepath, 'r', encoding="utf-8") as file:
            data = json.load(file)
        # Заполняем таблицы данными из файла
        try:
            with self.connect_to_database() as connection:
                connection.autocommit = True
                with connection.cursor() as cur:
                    for vacancy in data:
                        cur.execute(
                            """
                            INSERT INTO employers (employer_name) 
                            SELECT %s
                            WHERE NOT EXISTS (
                            SELECT employer_name 
                            FROM employers
                            WHERE employer_name = %s)
                            """,
                            (vacancy['employer'], vacancy['employer']))

                        cur.execute("SELECT employer_id FROM employers ORDER BY employer_id DESC LIMIT 1")
                        employer_id = cur.fetchone()

                        cur.execute(
                            """
                            INSERT INTO vacancies (employer_id, vacancy_title, vacancy_url, vacancy_area,
                            salary_from, salary_to)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (employer_id, vacancy['vacancy_title'], vacancy['vacancy_url'], vacancy['vacancy_area'],
                             vacancy['salary_from'], vacancy['salary_to']))

                print('Таблицы успешно заполнены')

            connection.close()

        except psycopg2.Error as e:
            print(f"Ошибка заполнения: {e}")

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        pass
