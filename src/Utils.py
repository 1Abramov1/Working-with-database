import json


class Utils:

    @staticmethod
    def reader_file(file_path: str) -> dict:
        """Метод для чтения данных из указанного файла"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Файл {file_path} содержит невалидный JSON. Будет возвращен пустой словарь.")
            return {}
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return {}

    @staticmethod
    def _uniq(path_file: str) -> list:
        """Метод для получения уникальных названий компаний из JSON файла"""
        data = Utils.reader_file(path_file)
        if not data:
            return []

        # Получаем список названий компаний (ключи верхнего уровня)
        companies = list(data.keys())
        return companies

    @staticmethod
    def get_vacancies_data(path_file: str) -> list:
        """Метод для преобразования данных о вакансиях в нужный формат"""
        data = Utils.reader_file(path_file)
        if not data:
            return []

        vacancies_list = []
        for company_name, company_data in data.items():
            employer_info = company_data.get('employer_info', {})
            vacancies = company_data.get('vacancies', [])

            for vacancy in vacancies:
                # Обрабатываем зарплату
                salary_data = vacancy.get('salary')
                salary_from = None
                salary_to = None
                currency = None

                if salary_data and isinstance(salary_data, str):
                    # Обрабатываем строковый формат зарплаты "от 85000 RUR"
                    if 'от' in salary_data:
                        try:
                            salary_parts = salary_data.split()
                            salary_from = int(salary_parts[1])
                            currency = salary_parts[2] if len(salary_parts) > 2 else 'RUR'
                        except (IndexError, ValueError):
                            pass
                    elif 'до' in salary_data:
                        try:
                            salary_parts = salary_data.split()
                            salary_to = int(salary_parts[1])
                            currency = salary_parts[2] if len(salary_parts) > 2 else 'RUR'
                        except (IndexError, ValueError):
                            pass
                    elif '-' in salary_data:
                        try:
                            salary_parts = salary_data.split()
                            range_parts = salary_parts[0].split('-')
                            salary_from = int(range_parts[0])
                            salary_to = int(range_parts[1])
                            currency = salary_parts[1] if len(salary_parts) > 1 else 'RUR'
                        except (IndexError, ValueError):
                            pass

                vacancy_data = {
                    "id": vacancy.get('id'),
                    "employer": company_name,
                    "name": vacancy.get('name'),
                    "description": vacancy.get('snippet'),
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency,
                    "url": vacancy.get('url')
                }
                vacancies_list.append(vacancy_data)

        return vacancies_list