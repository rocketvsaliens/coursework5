import requests
import json
import os
from config import area_code, max_count_vacancies, employer_ids, JSON_DATA_DIR


class HeadHunter:
    """Класс для работы с API HeadHunter"""

    _base_url = "https://api.hh.ru/vacancies"

    def __init__(self, vacancy_area=area_code, page=0, per_page=max_count_vacancies) -> None:
        """
        Инициализатор экземпляров класса для работы с API
        :param vacancy_area: область поиска -- по умолчанию по всей России
        :param page: страница поиска -- по умолчанию 0 (начальная)
        :param per_page: количество вакансий на страницу -- по умолчанию 50
        """
        self.vacancy_area = vacancy_area
        self.page = page
        self.per_page = per_page

    def __str__(self):
        return 'HeadHunter'

    def get_vacancies_by_api(self, vacancy_title: str, employers: list) -> list[dict] or list:
        """
        Выполняет сбор вакансий через API
        :param vacancy_title: название вакансии
        :param employers: список работодателей
        :return: общий список вакансий выбранных компаний
        """
        common_list_vacancies = []
        for employer_id in employer_ids:
            params = {
                'text': vacancy_title,
                'area': self.vacancy_area,
                'employer_id': employer_id,
                'per_page': self.per_page
            }
            response = requests.get(self._base_url, params=params)
            if response.status_code == 200:
                vacancies = response.json()['items']

                if vacancies:
                    list_vacancies = self.__class__.organize_vacancy_info(vacancies)
                    common_list_vacancies.extend(list_vacancies)

            else:
                print(f'Ошибка {response.status_code} при выполнении запроса')

        return common_list_vacancies

    @staticmethod
    def organize_vacancy_info(vacancy_data: list) -> list:
        """
        Организует данные о вакансиях в определённом виде
        :param vacancy_data: список вакансий, полученный через API
        :return: организованный список вакансий
        """

        organized_vacancy_list = []

        for vacancy in vacancy_data:
            vacancy_title = vacancy.get('name')
            employer = vacancy.get('employer')['name']
            employer_url = f"https://hh.ru/employer/{vacancy.get('employer')['id']}"
            vacancy_area = vacancy.get('area')['name']
            vacancy_url = f"https://hh.ru/vacancy/{vacancy.get('id')}"
            salary = vacancy.get('salary')
            if not salary:
                salary_from = 0
                salary_to = 0
                currency = ''
            else:
                salary_from = salary.get('from')
                salary_to = salary.get('to')
                if not salary_from:
                    salary_from = salary_to
                if not salary_to:
                    salary_to = salary_from
                currency = vacancy.get('salary')['currency']
            experience = vacancy.get('experience')['name']
            requirements = (vacancy.get('snippet')['requirement'])
            if requirements:
                requirements = requirements.strip().replace('<highlighttext>', '').replace('</highlighttext>', '')

            vacancy_info = {
                'vacancy_title': vacancy_title,
                'employer': employer,
                'employer_url': employer_url,
                'vacancy_area': vacancy_area,
                'vacancy_url': vacancy_url,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'experience': experience,
                'requirements': requirements
            }

            organized_vacancy_list.append(vacancy_info)

        return organized_vacancy_list

    @staticmethod
    def save_vacancies_to_json(vacancy_list, filename):
        """
        Сохраняет вакансии в JSON-файл
        :param vacancy_list: список с вакансиями
        :param filename: имя файла для сохранения вакансий
        """
        filename = os.path.join(JSON_DATA_DIR, filename)

        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                print(f"Ошибка при создании директории: {e}")
                return

        try:
            with open(filename, 'w') as file:
                json.dump(vacancy_list, file, indent=2, ensure_ascii=False)
            print(f"Данные успешно записаны в файл")
        except Exception as e:
            print(f"Ошибка при записи данных в файл: {e}")


if __name__ == '__main__':
    hh = HeadHunter()
    vacancies_list = hh.get_vacancies_by_api('менеджер', employer_ids)
    hh.save_vacancies_to_json(vacancies_list, 'data.json')
