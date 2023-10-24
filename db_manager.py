import psycopg2


class DBManager:
    """
    Класс предоставляет статические методы для получения информации о компаниях и вакансиях
    """

    @staticmethod
    def get_companies_and_vacancies_count(database_name: str, params: dict):
        """Считаем количество вакансий по каждой компании"""

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT employers.company_name, COUNT(vacancies.employer_id) AS vacancy_count
                    FROM employers
                    LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                    GROUP BY employers.company_name;
            """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    @staticmethod
    def get_all_vacancies(database_name: str, params: dict):
        """Выводим список всех вакансий, при этом делая слияние с базой работодателей"""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
            SELECT employers.company_name, title AS vacancy_title, vacancy_url, salary_from, salary_to FROM vacancies
            LEFT JOIN employers USING(employer_id);
            """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    @staticmethod
    def get_avg_salary(database_name: str, params: dict):
        """Рассчитываем среднюю зарплату.
         При этом используем следующую логику: если указано от и до, то берем среднее значение,
        если только от или только до, то пограничное"""
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT AVG(salary_from)::numeric AS average_salary_from FROM vacancies
                    WHERE salary_from IS NOT NULL;

            """)

            result = cur.fetchone()

        conn.commit()
        conn.close()

        return result[0] if result else None

    @staticmethod
    def get_vacancies_with_higher_salary(database_name: str, params: dict):
        """Показываем список вакансий, чья зарплата выше средней"""

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT employers.company_name, title AS vacancy_title, vacancy_url, salary_from
                    FROM vacancies 
                    INNER JOIN employers USING(employer_id)
                    WHERE salary_from > ( SELECT AVG (salary_from) FROM vacancies WHERE salary_from IS NOT NULL)
            """)

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result

    @staticmethod
    def get_vacancies_with_keyword(database_name: str, params: dict, keyword: str):
        """Делаем выборку вакансий по ключевому слову, переданному пользователем"""

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT employers.company_name, title AS vacancy_title, vacancy_url, salary_from, salary_to
                    FROM vacancies
                    LEFT JOIN employers USING(employer_id)
                    WHERE title LIKE %s
            """, ('%' + keyword + '%',))

            result = cur.fetchall()

        conn.commit()
        conn.close()

        return result