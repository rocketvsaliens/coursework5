import utils
from src.dbhandler import DBHandler


def main():
    utils.get_started()  # получаем вакансии

    utils.create_and_fill_database()  # создаём и заполняем БД

    db_handler = utils.work_with_database()  # создаём экземпляр класса для работы с БД

    utils.show_employers_and_vacancies_count(db_handler)  # показываем работодателей и число вакансий

    utils.show_all_vacancies_info(db_handler)  # показываем все вакансии

    utils.show_avg_salary(db_handler)  # показываем среднюю зарплату по вакансиям

    utils.show_highly_paid_vacancies(db_handler)  # показываем вакансии с з/п выше средней

    utils.show_vacancies_by_keyword(db_handler)  # показываем вакансии по ключевому слову


if __name__ == '__main__':
    main()
