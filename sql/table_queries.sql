CREATE TABLE IF NOT EXISTS employers (
    employer_id serial PRIMARY KEY,
    employer_name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_id serial PRIMARY KEY,
    employer_id int REFERENCES employers(employer_id) ON DELETE CASCADE,
    vacancy_title varchar(255) NOT NULL,
    vacancy_url varchar(150) NOT NULL,
    vacancy_area varchar(80),
    salary_from int,
    salary_to int,
    CONSTRAINT chk_salary_from CHECK(salary_from >= 0),
    CONSTRAINT chk_salary_to CHECK(salary_to >= 0)
);