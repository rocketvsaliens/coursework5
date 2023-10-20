from src.dbmanager import DBManager
from src.headhunter import HeadHunter
from config import employer_ids, JSON_FILE_NAME, DB_NAME, SQL_DATA_DIR


def main():
    hh = HeadHunter()
    vacancies_list = hh.get_vacancies_by_api(employer_ids)
    hh.save_vacancies_to_json(vacancies_list, JSON_FILE_NAME)

    db = DBManager()
    db.create_database(DB_NAME)
    db.create_table(SQL_DATA_DIR)
    db.insert_data_to_table(JSON_FILE_NAME)


if __name__ == '__main__':
    main()
