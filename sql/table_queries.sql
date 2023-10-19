CREATE TABLE IF NOT EXISTS employers (
    employer_id serial PRIMARY KEY,
    employer_name varchar NOT NULL,
    employer_url varchar(50)
);

CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_id serial PRIMARY KEY,
    employer_id integer REFERENCES employers (employer_id) ON DELETE CASCADE,
    vacancy_title varchar NOT NULL,
    vacancy_url varchar(50) NOT NULL,
    vacancy_area varchar(30),
    salary_from int,
    salary_to int,
    currency varchar(3),
    experience varchar(25),
    requirements varchar,
    CONSTRAINT chk_salary_from CHECK(salary_from >= 0),
    CONSTRAINT chk_salary_to CHECK(salary_to >= 0)
);