import psycopg2
from psycopg2 import Error
from config import Config


class DBManager:

    def __init__(self) -> None:

        """Инициализация подключения к базе данных"""

        self.conn = psycopg2.connect(**Config.config())
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[dict]:

        """Получить список всех компаний и их количества вакансий"""

        try:
            self.cur.execute(
                """
                SELECT e.name_employer, COUNT(v.vacancy_id) as vacancy_count
                FROM employers e
                LEFT JOIN vacancies v ON e.emp_id = v.emp_id
                GROUP BY e.name_employer
                """
            )
            results = self.cur.fetchall()
            return [{"название компании": row[0], "количество вакансий": row[1]} for row in results]
        except Error as e:
            print(f"Ошибка при получении компаний и количества вакансий: {e}")
            return []

    def get_all_vacancies(self) -> list[dict]:

        """Получить список всех вакансий с названием компании, названием вакансии, зарплатой и URL"""

        try:
            self.cur.execute(
                """
                SELECT e.name_employer, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.emp_id = e.emp_id
                """
            )
            results = self.cur.fetchall()
            return [
                {
                    "название компании": row[0],
                    "название вакансии": row[1],
                    "зарплата от": row[2],
                    "зарплата до": row[3],
                    "url": row[4],
                }
                for row in results
            ]
        except Error as e:
            print(f"Ошибка при получении всех вакансий: {e}")
            return []

    def get_avg_salary(self) -> float:

        """Получить среднюю зарплату по всем вакансиям"""

        try:
            self.cur.execute(
                """
                SELECT AVG(salary_from)
                FROM vacancies
                """
            )
            result = self.cur.fetchone()
            return round(float(result[0]), 2) if result[0] else 0
        except Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return 0

    def get_vacancies_with_higher_salary(self) -> list[dict]:

        """Получить вакансии с зарплатой выше средней"""

        try:
            self.cur.execute(
                """
                WITH avg_salary AS (
                    SELECT AVG(salary_from) as avg_sal
                    FROM vacancies
                )
                SELECT e.name_employer, v.title, v.salary_from, v.url
                FROM vacancies v
                JOIN employers e ON v.emp_id = e.emp_id
                WHERE v.salary_from > (SELECT avg_sal FROM avg_salary)
                """
            )
            results = self.cur.fetchall()
            return [
                {
                    "название компании": row[0],
                    "название вакансии": row[1],
                    "зарплата от": row[2],
                    "url": row[3],
                }
                for row in results
            ]
        except Error as e:
            print(f"Ошибка при получении вакансий с более высокой зарплатой: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> list[dict]:

        """Получить вакансии, содержащие ключевое слово в своем названии"""

        try:
            self.cur.execute(
                """
                SELECT e.name_employer, v.title, v.salary_from, v.url
                FROM vacancies v
                JOIN employers e ON v.emp_id = e.emp_id
                WHERE LOWER(v.title) LIKE LOWER(%s)
                """,
                (f"%{keyword.lower()}%",),
            )
            results = self.cur.fetchall()
            return [{"company": row[0], "vacancy": row[1], "salary": row[2], "url": row[3]} for row in results]
        except Error as e:
            print(f"Ошибка при получении вакансий с ключевым словом: {e}")
            return []
