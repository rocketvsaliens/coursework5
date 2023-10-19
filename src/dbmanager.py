import psycopg2
from config import config


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self):
        self.database_name = None

    def connect_to_database(self):
        params = config()
        return psycopg2.connect(dbname=self.database_name, **params)

    def create_database(self, dbname: str) -> None:
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
