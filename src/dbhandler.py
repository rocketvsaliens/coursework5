from src.dbmanager import DBManager


class DBHandler(DBManager):
    """Класс для работы с базой данных"""

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

    @DBManager.db_connection
    def get_avg_salary(self, conn):
        """
        Получает среднюю зарплату по вакансиям
        :param conn: соединение с базой данных
        """
        query = "SELECT CAST(AVG((salary_from+salary_to)/2) AS INT) FROM vacancies"
        with conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchone()[0]
        return res

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = """
                    SELECT employers.employer_name, vacancies.vacancy_title,
                    (vacancies.salary_from + vacancies.salary_to) / 2, vacancies.vacancy_url
                    FROM vacancies
                    JOIN employers ON vacancies.employer_id = employers.employer_id
                    WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > %s
                    ORDER BY employers.employer_name;
                    """
        params = (self.get_avg_salary(),)
        return self.__execute_query(query, params=params)

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :param keyword: слово для поиска по вакансиям
        """
        query = """
                    SELECT employers.employer_name, vacancies.vacancy_title,
                    (vacancies.salary_from + vacancies.salary_to) / 2, vacancies.vacancy_url
                    FROM vacancies
                    JOIN employers ON vacancies.employer_id = employers.employer_id
                    WHERE vacancy_title LIKE %s OR vacancy_title LIKE %s
                    ORDER BY employers.employer_name;
                    """
        params = (f"%{keyword}%", f"%{keyword.capitalize()}%")
        return self.__execute_query(query, params=params)

    @DBManager.db_connection
    def __execute_query(self, conn, query: str, params=None):
        """
        Метод, который соединяется с БД, выполняет запрос и возвращает все результаты запроса
        :param conn: соединение с базой данных
        :param query: запрос к базе данных
        :param params: дополнительные параметры запроса к БД
        """
        with conn.cursor() as cur:
            cur.execute(query, params)
            res = cur.fetchall()
        return res
