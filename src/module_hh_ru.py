import requests
import json
from datetime import datetime
import time
import os


class HHAPI:
    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.headers = {
            "User-Agent": "HH-API-Client/1.0"
        }

    def get_employer_id(self, employer_name):
        """Поиск ID работодателя по названию"""
        url = f"{self.base_url}/employers"
        params = {
            "text": employer_name,
            "only_with_vacancies": True,
            "per_page": 1
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data['items']:
                return data['items'][0]['id']
            else:
                print(f"Работодатель '{employer_name}' не найден")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при поиске работодателя {employer_name}: {e}")
            return None

    def get_employer_info(self, employer_id):
        """Получение информации о работодателе"""
        url = f"{self.base_url}/employers/{employer_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении информации о работодателе {employer_id}: {e}")
            return None

    def get_employer_vacancies(self, employer_id, per_page=50):
        """Получение вакансий работодателя (максимум 50)"""
        url = f"{self.base_url}/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": per_page,  # Ограничиваем количество вакансий
            "page": 0
        }

        vacancies = []

        try:
            # Получаем только первую страницу, чтобы не превысить лимит в 50 вакансий
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Берем не более 50 вакансий
            vacancies = data['items'][:per_page]

            return vacancies

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении вакансий работодателя {employer_id}: {e}")
            return []

    def process_salary(self, salary_data):
        """Обработка данных о зарплате"""
        if not salary_data:
            return None

        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency', 'RUR')

        if salary_from and salary_to:
            return f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        else:
            return None


def save_to_json(data, filename):
    """Сохраняет данные в JSON файл"""
    # Создаем папку data, если она не существует
    if not os.path.exists('..\data'):
        os.makedirs('data')
        print("Создана папка 'data'")

    filepath = os.path.join("..",'data', filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath


def main():
    # Список компаний для анализа
    companies = [
        "Сбербанк",
        "Альфабанк",
        "Т-Банк",
        "Газпром",
        "Мегафон",
        "Билайн",
        "МТС",
        "Яндекс",
        "Ozon",
        "Wildberries"
    ]

    hh_api = HHAPI()
    all_data = {}

    print("Начинаем сбор данных с HH API...")
    print("=" * 50)

    for company in companies:
        print(f"Обрабатываем: {company}")

        # Получаем ID работодателя
        employer_id = hh_api.get_employer_id(company)
        if not employer_id:
            print(f"❌ Не удалось найти ID для {company}")
            continue

        # Получаем информацию о работодателе
        employer_info = hh_api.get_employer_info(employer_id)
        if not employer_info:
            print(f"❌ Не удалось получить информацию о работодателе {company}")
            continue

        # Получаем вакансии (максимум 50)
        vacancies = hh_api.get_employer_vacancies(employer_id, per_page=5)

        # Сохраняем данные
        all_data[company] = {
            'employer_info': employer_info,
            'vacancies': vacancies
        }

        print(f"✓ Найдено вакансий: {len(vacancies)}")
        time.sleep(0.5)  # Задержка между запросами

        # Подготавливаем данные для сохранения
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"hh_data_{timestamp}.json"

    # Конвертируем данные в JSON-совместимый формат
    json_data = {}
    for company, data in all_data.items():
        # Проверяем, что employer_info не None
        employer_info = data['employer_info']
        if employer_info is None:
            print(f"⚠️ Пропускаем {company} - нет информации о работодателе")
            continue

        json_data[company] = {
            'employer_info': {
                'id': employer_info.get('id'),
                'name': employer_info.get('name'),
                'url': employer_info.get('alternate_url'),
                'logo': employer_info.get('logo_urls', {}).get('90') if employer_info.get('logo_urls') else None,
                'description': employer_info.get('description'),
                'area': employer_info.get('area', {}).get('name') if employer_info.get('area') else None,
                'open_vacancies': employer_info.get('open_vacancies')
            },
            'vacancies': []
        }

        for vacancy in data['vacancies']:
            processed_vacancy = {
                'id': vacancy.get('id'),
                'name': vacancy.get('name'),
                'url': vacancy.get('alternate_url'),
                'salary': hh_api.process_salary(vacancy.get('salary')),
                'experience': vacancy.get('experience', {}).get('name'),
                'employment': vacancy.get('employment', {}).get('name'),
                'schedule': vacancy.get('schedule', {}).get('name'),
                'published_at': vacancy.get('published_at'),
                'snippet': vacancy.get('snippet', {}).get('requirement')
            }
            json_data[company]['vacancies'].append(processed_vacancy)

    # Сохраняем в папку data
    filepath = save_to_json(json_data, filename)

    print("=" * 50)
    print(f"Данные сохранены в файл: {filepath}")

    # Выводим краткую статистику
    print("\nСтатистика:")
    print("-" * 30)
    total_vacancies = 0
    for company, data in json_data.items():
        vacancies_count = len(data['vacancies'])
        total_vacancies += vacancies_count
        print(f"{company}: {vacancies_count} вакансий")

    print(f"\nВсего вакансий: {total_vacancies}")
    print(f"Всего компаний: {len(json_data)}")


if __name__ == "__main__":
    main()