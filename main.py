from src.db_save import DBControllerCompanies, DBControllerVacancies
from src.db_manager import DBManager


def get_vacancies():
    # Функция для получения и сохранения вакансий в базу данных
    print("Начинаем сохранение данных в базу...")

    try:
        # Сначала сохраняем компании
        saver_employers = DBControllerCompanies()
        print("Сохраняем компании...")
        saver_employers.save()

        # Затем сохраняем вакансии
        saver_vacancies = DBControllerVacancies()
        print("Сохраняем вакансии...")
        saver_vacancies.save()

        print("Сохранение завершено!")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        raise


def main():
    # Главная функция программы
    print("Запуск программы...")

    try:
        # Сохраняем данные в базу данных
        get_vacancies()
        print("Данные успешно загружены!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return

    # Создаем менеджер для работы с БД
    db_manager = DBManager()

    while True:
        # Показываем пользователю меню
        print("\n" + "=" * 50)
        print("МЕНЮ ПРОГРАММЫ")
        print("=" * 50)
        print("1. Показать все компании и сколько у них вакансий")
        print("2. Показать все вакансии с зарплатами")
        print("3. Показать среднюю зарплату")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Найти вакансии по слову")
        print("6. Выйти")
        print("=" * 50)

        # Получаем выбор пользователя
        choice = input("Введите номер действия: ")

        # Обрабатываем выбор
        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"{company['название компании']}: {company['количество вакансий']} вакансий")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                salary_info = ""
                if vacancy['зарплата от'] or vacancy['зарплата до']:
                    if vacancy['зарплата от'] and vacancy['зарплата до']:
                        salary_info = f"{vacancy['зарплата от']} - {vacancy['зарплата до']}"
                    elif vacancy['зарплата от']:
                        salary_info = f"от {vacancy['зарплата от']}"
                    elif vacancy['зарплата до']:
                        salary_info = f"до {vacancy['зарплата до']}"
                else:
                    salary_info = "не указана"

                print(f"{vacancy['название компании']}: {vacancy['название вакансии']} - {salary_info}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(f"{vacancy['название компании']}: {vacancy['название вакансии']} - {vacancy['зарплата от']}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in vacancies:
                print(f"{vacancy['company']}: {vacancy['vacancy']} - {vacancy['salary']}")

        elif choice == "6":
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()