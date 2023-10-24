from typing import Any
import requests


def get_companies_data(company_names: list[str]) -> list[dict[str, Any]]:
    """Функция, использующая API для получения данных о компании и вакансиях"""
    # список словарей о компаниях и вакансиях
    data = []

    for name_company in company_names:
        url = 'https://api.hh.ru/employers'
        headers = {
            'User-Agent': 'MyApp/company_parser rmanvelovich@gmail.com'
        }
        params = {
            'text': {name_company}
        }

        # подключение к API hh.ru
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            json_data = response.json()

            # создание списка вакансий
            vacancies = []

            vacancies_url = json_data['items'][0]['vacancies_url']

            vacancies_response = requests.get(vacancies_url)

            if vacancies_response.status_code == 200:

                data_vacancies = vacancies_response.json()

                for vacancy in data_vacancies['items']:
                    vacancies.append(vacancy)

            data.append({
                'employer': json_data['items'][0],
                'vacancies': vacancies
            })
        else:
            raise Exception(f'Ошибка в запросе {name_company}')

    return data