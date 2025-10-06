import psycopg2
from config import Config
from src.Utils import Utils


class DBControllerCompanies:
      """ Класс для сохранения названия организаций в базу данных"""

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
                      self.cur.execute("INSERT INTO employers (name_employer) VALUES (%s)", (emp,))
                  self.conn.commit()
              print("Работодатели сохранены")
          except Exception as e:
              print(f"Ошибка при сохранении работодателей: {e}")



class DBControllerVacancies:
      """ Класс для сохранения вакансий"""
      pass