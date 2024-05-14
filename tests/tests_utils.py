import io
import unittest
from utils import get_data, sort_data_by_date, print_last_five_executed, blur_card, blur_account
from unittest import mock


class TestFunctions(unittest.TestCase):
    def setUp(self):
        # Prepare test data
        self.data = [
            {
                "date": "2024-05-14T12:30:00.000000",
                "state": "EXECUTED",
                "description": "Description 1",
                "from": "1234567890123456",
                "to": "Счет 1234567890",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                }
            },
            {
                "date": "2024-05-15T13:45:00.000000",
                "state": "EXECUTED",
                "description": "Description 2",
                "from": "Счет 1234567890",
                "to": "9876543210987654",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                }
            },
            {
                "date": "2024-05-16T14:50:00.000000",
                "state": "CANCELLED",
                "description": "Description 3",
                "from": "1234567890123456",
                "to": "9876543210987654"
            },
            {
                "date": "2024-05-17T15:55:00.000000",
                "state": "EXECUTED",
                "description": "Description 4",
                "from": "9876543210987654",
                "to": "Счет 1234567890"
            },
            {
                "date": "2024-05-18T16:20:00.000000",
                "state": "EXECUTED",
                "description": "Description 5",
                "from": "Счет 1234567890",
                "to": "1234567890123456"
            }
        ]

    def test_get_data(self):
        # Проверка функции get_data
        self.assertIsInstance(get_data(), list)

    def test_sort_data_by_date(self):
        # Проверка сортировки данных по дате
        sorted_data = sort_data_by_date(self.data)
        self.assertEqual(sorted_data[0]['description'], "Description 5")

    def test_print_last_five_executed(self):
        # Проверка вывода последних пяти выполненных операций
        # Сначала создаем объект для перенаправления вывода
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as fake_stdout:
            print_last_five_executed(self.data)
            output = fake_stdout.getvalue()
            # Проверяем, что вывод содержит информацию о выполненных операциях
            self.assertIn("Description 5", output)
            self.assertIn("Description 4", output)
            self.assertIn("Description 2", output)
            self.assertIn("Description 1", output)
            self.assertNotIn("Description 3", output)  # Проверка, что отмененная операция не выводится

    def test_blur_card(self):
        # Проверка функции замены определенных символов в номерах карт
        card_number = "Visa Gold 1234567890123456"
        self.assertEqual(blur_card(card_number), "Visa Gold 1234 56** **** 3456")

    def test_blur_account(self):
        # Проверка функции замены определенных символов в номерах счетов
        account_number = "Счет 1234567890123456"
        self.assertEqual(blur_account(account_number), "Счет ************3456")


