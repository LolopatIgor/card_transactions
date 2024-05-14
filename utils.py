import json
from datetime import datetime


def get_data():
    """Загружает данные об операциях из файла"""
    # Загрузка данных из файла operations.json
    with open('data/operations.json', 'r', encoding='UTF-8') as file:
        file_data = json.load(file)
    return file_data


def sort_data_by_date(my_data):
    """Сортирует операции по дате"""
    # Функция для извлечения даты из словаря
    def get_date(item):
        date_str = item.get('date', '')
        # Преобразование строки в объект datetime
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f') if date_str else datetime.min

    # Сортировка списка по дате в обратном порядке
    sorted_data = sorted(my_data, key=get_date, reverse=True)
    return sorted_data


def print_last_five_executed(my_data: list):
    """Выводит последние 5 операций """
    # Счетчик выполненных операций
    operations_count = 0
    # Счетчик элементов в списке данных
    dict_count = 0
    # Пока не выведено 5 выполненных операций и не достигнут конец списка
    while operations_count < 5 and dict_count < len(my_data):
        # Получение текущего словаря данных
        current_dict_data = my_data[dict_count]
        # Проверка, является ли операция выполненной
        if current_dict_data["state"].upper() == "EXECUTED":
            # Увеличение счетчика выполненных операций
            operations_count += 1
            # Вывод информации о выполненной операции
            print_element(current_dict_data)
        else:
            pass  # Не обрабатываем невыполненные операции

        # Увеличение счетчика для перехода к следующему элементу в списке данных
        dict_count += 1


def print_element(transaction_dict: dict):
    """Выводит одну транзакцию"""
    # Преобразование даты в нужный формат
    elem_date = datetime.strptime(transaction_dict["date"], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    # Извлечение описания операции
    elem_description = transaction_dict["description"]
    elem_from = ""
    elem_to = ""
    # Извлечение суммы операции
    if 'operationAmount' in transaction_dict:
        elem_amount = f"{transaction_dict['operationAmount']['amount']} {transaction_dict['operationAmount']['currency']['name']}"
    else:
        elem_amount = "N/A"

    if "from" in transaction_dict:
        if "СЧЕТ" in transaction_dict["from"].upper():
            elem_from = f"{blur_account(transaction_dict['from'])} -> "
        else:
            elem_from = f"{blur_card(transaction_dict['from'])} -> "

    if "СЧЕТ" in transaction_dict["to"].upper():
        elem_to = f"{blur_account(transaction_dict['to'])}"
    else:
        elem_to = f"{blur_card(transaction_dict['to'])}"

    # Вывод информации об операции
    print(f"{elem_date} {elem_description}")
    print(f"{elem_from}{elem_to}")
    print(elem_amount)
    print("")


def blur_card(card_data: str):
    """Прячет полный номер карты"""
    # Получение первой части с названием карты
    first_part = card_data[:-16]
    # Получение второй части с номером карты
    second_part = card_data[-16:]
    second_part_coded = ""

    for i in range(len(second_part)):
        if i in range(6, 12):  # Индексы, которые нужно заменить на '*'
            second_part_coded += "*"
        else:
            second_part_coded += second_part[i]

        if i == 3 or i == 7 or i == 11:  # Добавление пробелов после каждых 4 символов
            second_part_coded += " "

    return f"{first_part}{second_part_coded}"


def blur_account(account_data: str):
    """Прячет полный номер счёта"""
    # Получение первой части со счетом
    first_part = account_data[:5]
    # Получение второй части с номером счета
    second_part = account_data[5:]
    second_part_coded = ""

    for i in range(len(second_part)):
        if i in range(len(second_part) - 4):  # Индексы, которые нужно заменить на '*'
            second_part_coded += "*"
        else:
            second_part_coded += second_part[i]

    return f"{first_part}{second_part_coded}"
