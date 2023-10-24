from config import config
from db_manager import DBManager


def for_user():
    """Функция для пользователя"""

    # переменная конфигурация, хранящая данные для подключения к БД
    parameters = config()

    while True:
        print("Что вы ищите?:")
        print("1 - Список всех компаний и свободные вакансии")
        print("2 - Список всех вакансий с указанием названия компании,вакансии,зарплаты и ссылки на вакансию")
        print("3 - Узнатьреднюю зарплату по вакансиям")
        print("4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5 - Показать список вакансий, в названии которых содержатся переданные слова, например 'Python'")
        print("0 - Завершить программу")

        # Создаем экземпляр класса DBManager
        db_manager = DBManager()

        choice = input("Введите номер действия: ")

        if choice == "1":

            result = db_manager.get_companies_and_vacancies_count('kurs5', parameters)
            for el in result:
                print(el)

        elif choice == "2":
            print("None означает,что зарплата не указана")

            result = db_manager.get_all_vacancies('kurs5', parameters)
            for el in result:
                print(el)

        elif choice == "3":
            print("Средняя считается по нижней вилке")

            salary = db_manager.get_avg_salary('kurs5', parameters)
            round_salary = round(salary)
            print(f'Средняя зарплата по вакансиям равна- {round_salary} RUB')

        elif choice == "4":

            result = db_manager.get_vacancies_with_higher_salary('kurs5', parameters)
            for el in result:
                print(el)

        elif choice == "5":

            user_keyword = input('Введите ключевое слово для поиска: ')

            result = db_manager.get_vacancies_with_keyword('kurs5', parameters, user_keyword)
            if result:
                for el in result:
                    print(el)
            else:
                print(f'По слову {user_keyword} не найдено вакансий')

        elif choice == "0":
            print("Завершение программы...")
            print("До свидания! Ждем Вас снова!")
            exit()
        else:
            print("Нет такого варианта. Введите другой вариант")