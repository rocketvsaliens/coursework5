from src.dbmanager import DBManager
from config import JSON_FILE_NAME, DB_NAME, SQL_DATA_DIR
from utils import (get_started, show_employers_and_vacancies_count, show_all_vacancies_info,
                   show_avg_salary, show_highly_paid_vacancies, show_vacancies_by_keyword)


def main():
    get_started()  # получаем вакансии

    db = DBManager()
    db.create_database(DB_NAME)  # создаём БД
    db.create_table(SQL_DATA_DIR)  # создаём таблицы в БД
    db.insert_data_to_table(JSON_FILE_NAME)  # заполняем таблицы

    show_employers_and_vacancies_count(db)  # показываем работодателей и число вакансий

    show_all_vacancies_info(db)  # показываем все вакансии

    show_avg_salary(db)  # показываем среднюю зарплату по вакансиям

    show_highly_paid_vacancies(db)  # показываем вакансии с з/п выше средней

    show_vacancies_by_keyword(db)  # показываем вакансии по ключевому слову


if __name__ == '__main__':
    main()
