import psycopg2


def create_database(database_name: str, params: dict):
    """Создание базы данных и подключение к ней"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    company_url VARCHAR UNIQUE NOT NULL
                );
        """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    employer_id int REFERENCES employers(employer_id),
                    vacancy_id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    city VARCHAR(255),
                    vacancy_url VARCHAR UNIQUE,
                    salary_from int NULL,
                    salary_to int NULL,
                    description text
                );
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list, database_name: str, params: dict):
    """Сохранение данных в базе данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            company_data = company['employer']
            cur.execute(
                """
                INSERT INTO employers (company_name, company_url)
                VALUES (%s, %s)
                RETURNING employer_id
                """,
                (company_data['name'], company_data['alternate_url'])
            )
            employer_id = cur.fetchone()[0]

            vacancies = company['vacancies']

            for vacancy in vacancies:
                vacancies_data = vacancy

                salary = vacancies_data.get('salary', None)
                salary_from = salary.get('from', None) if salary else None
                salary_to = salary.get('to', None) if salary else None

                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, title, city, vacancy_url, 
                    salary_from, salary_to, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancies_data['name'], vacancies_data['area']['name'],
                     vacancies_data['alternate_url'], salary_from, salary_to,
                     vacancies_data['snippet']['responsibility'])
                )

    conn.commit()
    conn.close()