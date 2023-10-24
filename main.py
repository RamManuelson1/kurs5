from utils import create_database, save_data_to_database
from api_hh import get_companies_data
from config import config


def main():
    """Основная функция для запуска программы"""
    parameters = config()

    name_companies = [
        'Тинькофф',
        'Яндекс',
        'Mail.ru',
        'Газпром нефть',
        'BMW',
        'ВКонтакте',
        'Inventive Retail Group',
        'ЛУКОЙЛ',
        '2GIS Поволжье',

    ]

    data = get_companies_data(name_companies)
    create_database('coursework_5', parameters)
    save_data_to_database(data, 'coursework_5', parameters)


if __name__ == '__main__':
    main()