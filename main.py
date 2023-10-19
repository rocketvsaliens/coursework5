from src.dbmanager import DBManager
from config import SQL_DATA_DIR


def main():
    db = DBManager()
    db.create_database('headhunter')
    db.create_table(SQL_DATA_DIR)


if __name__ == '__main__':
    main()
