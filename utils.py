from src.headhunter import HeadHunter
from src.dbmanager import DBManager
from src.dbhandler import DBHandler
from config import employer_ids, employer_ids_krd, JSON_FILE_NAME, SQL_DATA_DIR


def get_started():
    """
    Функция для начала работы с вакансиями.
    Получает вакансии из введённого пользователем региона и записывает их в файл
    """
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


def create_and_fill_database():
    """Создаёт базу данных с указанным пользователем именем и заполняет её данными из json"""
    while True:
        db_name = input('Введите слово на английском для названия базы данных: ')
        if (all(one_letter in 'abcdefghijklmnopqrstuvwxyz1234567890' for one_letter in db_name)
                and not db_name.isdigit()):
            db = DBManager()
            break
        else:
            print("Некорректный ввод. Проверьте раскладку и отсутствие кавычек. "
                  "Имя БД должно содержать буквы или буквы и цифры")
    db.create_database(db_name)  # создаём БД
    db.create_table(SQL_DATA_DIR)  # создаём таблицы в БД
    db.insert_data_to_table(JSON_FILE_NAME)  # заполняем таблицы

    return db


def work_with_database():
    while True:
        choice = input('Желаете получить сведения из базы данных? (1 - да, 0 - нет): ')
        if choice == '1':
            handler = DBHandler()
            return handler
        elif choice == '0':
            print('Не смею вас больше задерживать. Хорошего дня!')
            exit(0)
        else:
            print('Неверный ввод')
            continue


def show_employers_and_vacancies_count(db_manager):
    """
    Выводит всех работодателей и количество вакансий от них
    :param db_manager: экземпляр класса для работы с БД
    """
    choice = input('Показать всех работодателей и количество вакансий от каждого? (1 - да): ')
    if choice == '1':
        list_employers_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
        for one_employer in list_employers_and_vacancies_count:
            print(f'Получено {one_employer[1]} вакансий от работодателя {one_employer[0]}')
    else:
        print('Для продолжения нажмите любую клавишу')
        input()


def show_all_vacancies_info(db_manager):
    """
    Выводит информацию по всем вакансиям
    :param db_manager: экземпляр класса для работы с БД
    """
    choice = input('Показать всех работодателей и количество вакансий от каждого? (1 - да): ')
    if choice == '1':
        all_vacancies_list = db_manager.get_all_vacancies()
        for one_vacancy in all_vacancies_list:
            print(*one_vacancy, sep=' | ')
    else:
        print('Для продолжения нажмите любую клавишу')
        input()


def show_avg_salary(db_manager):
    """
    Выводит среднюю зарплату по всем вакансиям
    :param db_manager: экземпляр класса для работы с БД
    """
    choice = input('Показать среднюю зарплату по всем вакансиям? (1 - да): ')
    if choice == '1':
        print(f'\nСредняя зарплата по вакансиям равна {db_manager.get_avg_salary()} руб.\n')
    else:
        print('Для продолжения нажмите любую клавишу')
        input()


def show_highly_paid_vacancies(db_manager):
    """
    Выводит информацию по вакансиям с з/п выше средней
    :param db_manager: экземпляр класса для работы с БД
    """
    choice = input('Показать вакансии с з/п выше средней? (1 - да): ')
    if choice == '1':
        print('\nВот наиболее высокооплачиваемые вакансии:\n')
        vacancies_with_high_salary = db_manager.get_vacancies_with_higher_salary()
        for one_vacancy in vacancies_with_high_salary:
            print(*one_vacancy, sep=' | ')
    else:
        print('Для продолжения нажмите любую клавишу')
        input()


def show_vacancies_by_keyword(db_manager):
    """
    Выводит все вакансии, в названии которых есть ключевое слово
    :param db_manager: экземпляр класса для работы с БД
    """
    keyword = input('Введите ключевое слово для поиска в названиях вакансий: ')
    if keyword:

        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
        if vacancies_with_keyword:
            print('\nВот вакансии по вашему запросу:\n')
            for one_vacancy in vacancies_with_keyword:
                print(*one_vacancy, sep=' | ')
        else:
            print('По вашему запросу не нашлось вакансий')

    else:
        print('Вот и все опции. Спасибо, что выбрали нашу программу ;)')
