from src.db_save import DBControllerCompanies, DBControllerVacancies


def get_vacancies():
    # Функция для получения и сохранения вакансий в базу данных
    print("Начинаем сохранение данных в базу...")

    # Создаем объекты для сохранения работодателей и вакансий
    saver_employers = DBControllerCompanies()
    saver_vacancies = DBControllerVacancies()

    # Собираем их в список
    savers = [saver_employers, saver_vacancies]

    # Проходим по списку и сохраняем данные
    for saver in savers:
        print(f"Сохраняем {type(saver).__name__}...")
        saver.save()

    print("Сохранение завершено!")


def main():
    # Главная функция программы
    print("Запуск программы...")

    try:
        # Сначала парсим вакансии с сайта

        # Потом сохраняем их в базу данных
        get_vacancies()
        print("Данные успешно загружены!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return

    while True:
        # Показываем пользователю меню
        print("\n" + "="*50)
        print("МЕНЮ ПРОГРАММЫ")
        print("="*50)
        print("1. Показать все компании и сколько у них вакансий")
        print("2. Показать все вакансии с зарплатами")
        print("3. Показать среднюю зарплату")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Найти вакансии по слову")
        print("6. Выйти")
        print("="*50)

        # Получаем выбор пользователя
        choice = input("Введите номер действия: ")

        # Обрабатываем выбор
        if choice == "1":
             pass

if __name__ == "__main__":
    main()