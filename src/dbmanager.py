import psycopg2
import json
import os
from config import config, JSON_DATA_DIR


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self):
        self.database_name = None

    def __connect_to_database(self):
        """Метод для подключения к базе данных"""
        params = config()
        return psycopg2.connect(dbname=self.database_name, **params)

    def create_database(self, dbname: str) -> None:
        """
        Метод для создания базы данных
        :param dbname: имя создаваемой базы данных
        """
        try:
            connection = self.__connect_to_database()
            connection.autocommit = True

            with connection.cursor() as cur:
                cur.execute(f'DROP DATABASE IF EXISTS {dbname}')
                cur.execute(f'CREATE DATABASE {dbname}')
                self.database_name = dbname
                print(f'База данных {dbname} успешно создана')

            connection.close()

        except psycopg2.OperationalError as e:
            print(f'Ошибка создания базы данных: {e}')

    def create_table(self, db_queries_file: str) -> None:
        """
        Метод для создания таблиц в базе данных
        :param db_queries_file: файл с запросами на создание таблиц в БД
        """
        try:
            with self.__connect_to_database() as connection:

                with open(db_queries_file, 'r', encoding='utf-8') as file:
                    create_table_query = file.read()

                with connection.cursor() as cur:
                    cur.execute(create_table_query)
                    print(f'Таблицы в базе {self.database_name} успешно созданы')
            connection.commit()
            connection.close()

        except psycopg2.OperationalError as e:
            print(f'Ошибка создания таблицы: {e}')

    def insert_data_to_table(self, data_filename: str) -> None:
        """
        Метод для заполнения таблиц в базе данных из файла json
        :param data_filename: файл json с данными
        """

        filepath = os.path.join(JSON_DATA_DIR, data_filename)
        with open(filepath, 'r', encoding="utf-8") as file:
            data = json.load(file)

        try:
            with self.__connect_to_database() as connection:
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

                print(f'Таблицы успешно заполнены данными из файла {data_filename}')

            connection.close()

        except psycopg2.Error as e:
            print(f'Ошибка заполнения таблицы: {e}')

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = """
                SELECT employers.employer_name, COUNT(*) from employers
                JOIN vacancies USING (employer_id)
                GROUP BY employers.employer_name
                ORDER BY employers.employer_name
                """

        return self.__execute_query(query)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        query = """
                SELECT employers.employer_name, vacancies.vacancy_title,
                (vacancies.salary_from + vacancies.salary_to) / 2 AS average_salary, vacancies.vacancy_url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                ORDER BY employers.employer_name;
                """
        return self.__execute_query(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query = "SELECT CAST(AVG((salary_from+salary_to)/2) AS INT) FROM vacancies"
        with self.__connect_to_database() as connection:
            with connection.cursor() as cur:
                cur.execute(query)
                res = cur.fetchone()[0]
        connection.close()
        return res

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        query = f"""
                SELECT employers.employer_name, vacancies.vacancy_title,
                (vacancies.salary_from + vacancies.salary_to) / 2, vacancies.vacancy_url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > {avg_salary}
                ORDER BY employers.employer_name;
                """
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f"""
                SELECT employers.employer_name, vacancies.vacancy_title,
                (vacancies.salary_from + vacancies.salary_to) / 2, vacancies.vacancy_url
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE vacancy_title LIKE '%{keyword}%' OR vacancy_title LIKE '%{keyword.capitalize()}%'
                ORDER BY employers.employer_name;
                """
        return self.__execute_query(query)

    def __execute_query(self, query):
        """
        Метод, который соединяется с БД, выполняет запрос и возвращает все результаты запроса
        :param query: запрос к базе данных
        """
        with self.__connect_to_database() as connection:
            with connection.cursor() as cur:
                cur.execute(query)
                res = cur.fetchall()
        connection.close()
        return res
