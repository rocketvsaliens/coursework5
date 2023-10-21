from src.dbmanager import DBManager
from src.headhunter import HeadHunter
from config import employer_ids, employer_ids_krd, JSON_FILE_NAME, DB_NAME, SQL_DATA_DIR


def main():
    while True:
        choice = input('Введите код региона для поиска вакансий (113 - вся Россия, 53 - Краснодар): ')
        if choice == '113':
            hh = HeadHunter()
            vacancies_list = hh.get_vacancies_by_api(employer_ids)
            hh.save_vacancies_to_json(vacancies_list, JSON_FILE_NAME)
            break
        elif choice == '53':
            hh = HeadHunter(vacancy_area=53)
            vacancies_list = hh.get_vacancies_by_api(employer_ids_krd)
            hh.save_vacancies_to_json(vacancies_list, JSON_FILE_NAME)
            break
        else:
            print('Неверный ввод')
            continue

    db = DBManager()
    db.create_database(DB_NAME)
    db.create_table(SQL_DATA_DIR)
    db.insert_data_to_table(JSON_FILE_NAME)

    list_employers_and_vacancies_count = db.get_companies_and_vacancies_count()
    for one_employer in list_employers_and_vacancies_count:
        print(f'Получено {one_employer[1]} вакансий от компании {one_employer[0]}')

    all_vacancies_list = db.get_all_vacancies()
    for one_vacancy in all_vacancies_list:
        print(*one_vacancy, sep=' | ')

    print(db.get_avg_salary())

    vacancies_with_high_salary = db.get_vacancies_with_higher_salary()
    for one_vacancy in vacancies_with_high_salary:
        print(*one_vacancy, sep=' | ')

    keyword = input('Введите ключевое слово: ')
    vacancies_with_keyword = db.get_vacancies_with_keyword(keyword)
    if vacancies_with_keyword:
        for one_vacancy in vacancies_with_keyword:
            print(*one_vacancy, sep=' | ')
    else:
        print('По вашему запросу не нашлось вакансий')


if __name__ == '__main__':
    main()
