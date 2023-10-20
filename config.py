from configparser import ConfigParser
import os

# Яндекс, Билайн, МТС, Kaspersky, Tinkoff, Ozon, СБЕР, Fplus, Аэрофлот, РЖД
employer_ids = [1740, 4934, 3776, 1057, 78638, 2180, 3529, 6836, 1373, 23427]

# СБЕР, Магнит, X5 Group, Альфа-банк, ДНС, МВидео, Ситилинк, Фикспрайс, Роснефть, Агрокомплекс, НАО Красная Поляна
# employer_ids = [3529, 49357, 4233, 80, 1025275, 2523, 3148, 196621, 1312952, 247279, 1124351]

area_code = 113  # 53 - Краснодар

max_count_vacancies = 10

JSON_DATA_DIR = os.path.join('data')
JSON_FILE_NAME = 'data.json'
DB_NAME = 'headhunter'
SQL_DATA_DIR = os.path.join('sql', 'table_queries.sql')


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
