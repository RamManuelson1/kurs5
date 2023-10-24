--Создание базы данныхCREATE DATABASE database_name;

CREATE TABLE employers (
employer_id int PRIMARY KEY,
company_name VARCHAR(255) NOT NULL,
company_url VARCHAR UNIQUE NOT NULL
);

-- Создание таблицы с вакансиями этих работодателей
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

-- Получение списка компаний и вакансий этих компаний
SELECT employers.company_name, COUNT(vacancies.employer_id) AS vacancy_count
FROM employers
LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
GROUP BY employers.company_name;



--Получение списка всех вакансий с указанием названия компании, должности и заработной платы, а также ссылок на вакансию
SELECT employers.company_name, title AS vacancy_title, vacancy_url, salary_from, salary_to FROM vacancies
LEFT JOIN employers USING(employer_id);

--Получение средней зарплаты по вакансиям
SELECT AVG(salary_from) AS average_salary_from FROM vacancies
WHERE salary_from IS NOT NULL;



-- Список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT employers.company_name, title AS vacancy_title, vacancy_url, salary_from
FROM vacancies
INNER JOIN employers USING(employer_id)
WHERE salary_from > (
    SELECT AVG(salary_from)
    FROM vacancies
    WHERE salary_from IS NOT NULL
);


-- Список всех вакансий, в названии которых содержатся переданные в метод слова, например python
SELECT employers.company_name, title AS vacancy_title, vacancy_url, salary_from, salary_to
FROM vacancies
LEFT JOIN employers USING(employer_id)
WHERE title LIKE '%keyword%';