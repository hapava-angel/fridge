# test.py
import unittest
from decimal import Decimal
from datetime import date, timedelta

from main import Frige

class TestAdd(unittest.TestCase):
    def setUp(self):
        self.goods = {}

    def test_none_expiration_date(self):
        Frige.add(self.goods, "Пельмени", Decimal("1"), None)
        self.assertIn("Пельмени", self.goods)
        self.assertIsNone(self.goods["Пельмени"][0]["expiration_date"])

    def test_add_with_all_parameters(self):
        Frige.add(self.goods, "Хлеб", Decimal("2"), "2025-09-29")
        self.assertIn("Хлеб", self.goods)
        batch = self.goods["Хлеб"][0]
        self.assertEqual(batch["amount"], Decimal("2"))
        self.assertIsInstance(batch["expiration_date"], date)

    def test_add_only_required_parameters(self):
        Frige.add(self.goods, "Масло", Decimal("1"))
        self.assertIn("Масло", self.goods)
        batch = self.goods["Масло"][0]
        self.assertEqual(batch["amount"], Decimal("1"))
        self.assertIsNone(batch["expiration_date"])

    def test_add_with_incorrect_parameters(self):
        with self.assertRaises(ValueError):
            Frige.add(self.goods, "Масло", Decimal("-2"))


class TestAddByNote(unittest.TestCase):
    def setUp(self):
        self.goods = {}

    def test_note_without_expiration_date(self):
        Frige.add_by_note(self.goods, "Пельмени 1")
        self.assertIn("Пельмени", self.goods)
        batch = self.goods["Пельмени"][0]
        self.assertEqual(batch["amount"], Decimal("1"))
        self.assertIsNone(batch["expiration_date"])

    def test_add_by_note_with_all_parameters(self):
        Frige.add_by_note(self.goods, "Хлеб 2 2025-09-29")
        self.assertIn("Хлеб", self.goods)
        batch = self.goods["Хлеб"][0]
        self.assertEqual(batch["amount"], Decimal("2"))
        self.assertIsInstance(batch["expiration_date"], date)

    def test_add_by_note_only_required(self):
        Frige.add_by_note(self.goods, "Масло 1")
        self.assertIn("Масло", self.goods)
        batch = self.goods["Масло"][0]
        self.assertEqual(batch["amount"], Decimal("1"))
        self.assertIsNone(batch["expiration_date"])

    def test_add_by_note_incorrect_note(self):
        with self.assertRaises(ValueError):
            Frige.add_by_note(self.goods, "Масло много")


class TestFind(unittest.TestCase):
    def setUp(self):
        self.goods = {
            "Сыр": [{"amount": Decimal("1"), "expiration_date": None}],
            "Сырники": [{"amount": Decimal("2"), "expiration_date": date.today()}],
            "Хлеб": [{"amount": Decimal("3"), "expiration_date": date.today()}],
        }

    def test_find_requires_dict_and_string(self):
        with self.assertRaises(TypeError):
            Frige.find("Сыр", "Сыр")

    def test_find_exact_match(self):
        result = Frige.find(self.goods, "Хлеб")
        self.assertEqual(result, ["Хлеб"])

    def test_find_case_insensitive_partial(self):
        result = Frige.find(self.goods, "сыр")
        self.assertIn("Сыр", result)
        self.assertIn("Сырники", result)

    def test_find_no_result(self):
        result = Frige.find(self.goods, "манка")
        self.assertEqual(result, [])

class TestAmount(unittest.TestCase):
    def setUp(self):
        self.goods = {
            "Сыр": [
                {"amount": Decimal("1"), "expiration_date": None},
                {"amount": Decimal("2"), "expiration_date": date.today()},
            ],
            "Хлеб": [
                {"amount": Decimal("3"), "expiration_date": date.today()},
            ],
        }

    def test_amount_format(self):
        result = Frige.amount(self.goods, "Молоко")
        self.assertIsInstance(result, Decimal)

    def test_amount_single_product(self):
        result = Frige.amount(self.goods, "Хлеб")
        self.assertEqual(result, Decimal("3"))

    def test_amount_multiple_batches(self):
        result = Frige.amount(self.goods, "Сыр")
        self.assertEqual(result, Decimal("3"))

    def test_amount_no_products(self):
        result = Frige.amount(self.goods, "кукурузные палочки")
        self.assertEqual(result, Decimal("0"))


class TestExpire(unittest.TestCase):
    def setUp(self):
        self.today = date.today()
        self.goods = {
            "Сыр": [
                {"amount": Decimal("1"), "expiration_date": None},
                {"amount": Decimal("2"), "expiration_date": self.today - timedelta(days=1)},
            ],
            "Сырники": [
                {"amount": Decimal("2"), "expiration_date": self.today + timedelta(days=2)},
            ],
            "Хлеб": [
                {"amount": Decimal("3"), "expiration_date": self.today + timedelta(days=1)},
            ],
        }

    def test_expire_without_in_advance_days(self):
        result = Frige.expire(self.goods)
        self.assertIsInstance(result, list)

    def test_expire_correct_output_expired_only(self):
        result = Frige.expire(self.goods, in_advance_days=0)
        self.assertIn(("Сыр", Decimal("2")), result)
        titles = [name for name, _ in result]
        self.assertNotIn("Сырники", titles)
        self.assertNotIn("Хлеб", titles)

    def test_expire_correct_output_in_advance(self):
        result = Frige.expire(self.goods, in_advance_days=2)
        expected = {
            "Сыр": Decimal("2"),
            "Хлеб": Decimal("3"),
            "Сырники": Decimal("2"),
        }
        self.assertEqual(dict(result), expected)

    def test_expire_ignores_none_expiration(self):
        result = Frige.expire(self.goods, in_advance_days=10)
        total_syr = dict(result)["Сыр"]
        self.assertEqual(total_syr, Decimal("2"))


if __name__ == "__main__":
    unittest.main()