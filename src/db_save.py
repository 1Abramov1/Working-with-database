import psycopg2
from config import Config
from src.Utils import Utils


class DBControllerCompanies:
    """ Класс для сохранения названия организаций в базу данных"""

    def __init__(self):
        """Инициализация подключения к БД и пути к файлу"""
        self.conn = psycopg2.connect(**Config.config())
        self.cur = self.conn.cursor()
        self.path_file = "data/hh_data_20251001_221155.json"

    def _create_table(self) -> None:
        """Создание таблицы работодателей"""
        try:
            with self.conn:
                self.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS employers (
                        emp_id SERIAL PRIMARY KEY,
                        name_employer VARCHAR(100) NOT NULL UNIQUE
                    )
                    """
                )
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")

    def save(self) -> None:
        """Сохранение работодателей в базу данных"""
        self.emps = Utils._uniq(self.path_file)
        self._create_table()
        try:
            with self.conn:
                for emp in self.emps:
                    self.cur.execute(
                        "INSERT INTO employers (name_employer) VALUES (%s) ON CONFLICT (name_employer) DO NOTHING",
                        (emp,)
                    )
                self.conn.commit()
            print("Работодатели сохранены")
        except Exception as e:
            print(f"Ошибка при сохранении работодателей: {e}")


class DBControllerVacancies:
    """Класс для сохранения вакансий в базу данных"""

    def __init__(self):
        """Инициализация подключения к БД и пути к файлу"""
        self.conn = psycopg2.connect(**Config.config())
        self.cur = self.conn.cursor()
        self.path_file = "data/hh_data_20251001_221155.json"
        self.vacancies = Utils.get_vacancies_data(self.path_file)

    def _create_table(self) -> None:
        """Создание таблицы вакансий"""
        try:
            with self.conn:
                self.cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id VARCHAR(30) PRIMARY KEY,
                        emp_id INTEGER REFERENCES employers(emp_id),
                        title VARCHAR(100) NOT NULL,
                        description TEXT,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(3),
                        url VARCHAR(150)
                    )
                    """
                )
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")

    def save(self) -> None:
        """Сохранение вакансий в базу данных"""
        self._create_table()
        try:
            with self.conn:
                for vacancy in self.vacancies:
                    self.cur.execute(
                        "SELECT emp_id FROM employers WHERE name_employer = %s",
                        (vacancy.get("employer"),)
                    )
                    result = self.cur.fetchone()
                    if result:
                        emp_id = result[0]
                        self.cur.execute(
                            """
                            INSERT INTO vacancies (
                                vacancy_id,
                                emp_id,
                                title,
                                description,
                                salary_from,
                                salary_to,
                                currency,
                                url
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (vacancy_id) DO NOTHING
                            """,
                            (
                                vacancy.get("id"),
                                emp_id,
                                vacancy.get("name"),
                                vacancy.get("description"),
                                vacancy.get("salary_from"),
                                vacancy.get("salary_to"),
                                vacancy.get("currency"),
                                vacancy.get("url"),
                            ),
                        )
                self.conn.commit()
            print("Вакансии сохранены")
        except Exception as e:
            print(f"Ошибка при сохранении вакансий: {e}")