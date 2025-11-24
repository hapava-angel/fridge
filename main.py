from decimal import Decimal
from datetime import date, datetime, timedelta


class Frige:
    @staticmethod
    def add(items, title, amount, expiration_date=None):
        if not isinstance(items, dict):
            raise TypeError("items must be dict")
        if not isinstance(title, str):
            raise TypeError("title must be str")
        if not isinstance(amount, Decimal):
            raise TypeError("amount must be Decimal")
        if amount <= 0:
            raise ValueError("amount must be positive")

        exp = None
        if expiration_date is not None:
            if not isinstance(expiration_date, str):
                raise TypeError("expiration_date must be str or None")
            try:
                exp = datetime.strptime(expiration_date, "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError("invalid expiration_date format") from e

        batch = {"amount": amount, "expiration_date": exp}
        items.setdefault(title, []).append(batch)

    @staticmethod
    def add_by_note(items, note):
        if not isinstance(items, dict):
            raise TypeError("items must be dict")
        if not isinstance(note, str):
            raise TypeError("note must be str")

        parts = note.split()
        if len(parts) < 2:
            raise ValueError("note must contain at least title and amount")

        exp_str = None
        amount_index = len(parts) - 1

        last = parts[-1]
        try:
            if "-" in last:
                datetime.strptime(last, "%Y-%m-%d")
                exp_str = last
                amount_index = len(parts) - 2
        except ValueError:
            exp_str = None
            amount_index = len(parts) - 1

        if amount_index <= 0:
            raise ValueError("note must contain title and amount")

        title = " ".join(parts[:amount_index])
        amount_token = parts[amount_index]

        try:
            amount_dec = Decimal(amount_token)
        except Exception as e:
            raise ValueError("invalid amount in note") from e

        if amount_dec <= 0:
            raise ValueError("amount must be positive")

        Frige.add(items, title, amount_dec, exp_str)

    @staticmethod
    def find(items, needle):
        if not isinstance(items, dict):
            raise TypeError("items must be dict")
        if not isinstance(needle, str):
            raise TypeError("needle must be str")

        needle_lower = needle.lower()
        return [title for title in items.keys() if needle_lower in title.lower()]

    @staticmethod
    def amount(items, needle):
        if not isinstance(items, dict):
            raise TypeError("items must be dict")
        if not isinstance(needle, str):
            raise TypeError("needle must be str")

        needle_lower = needle.lower()
        total = Decimal("0")

        for title, batches in items.items():
            if needle_lower in title.lower():
                for batch in batches:
                    total += batch["amount"]

        return total

    @staticmethod
    def expire(items, in_advance_days=0):
        if not isinstance(items, dict):
            raise TypeError("items must be dict")
        if not isinstance(in_advance_days, int):
            raise TypeError("in_advance_days must be int")
        if in_advance_days < 0:
            raise ValueError("in_advance_days must be non-negative")

        today = date.today()
        border = today + timedelta(days=in_advance_days)
        totals = {}

        for title, batches in items.items():
            for batch in batches:
                exp = batch.get("expiration_date")
                if exp is None:
                    continue
                if not isinstance(exp, date):
                    raise TypeError("expiration_date must be date or None")
                if exp <= border:
                    totals[title] = totals.get(title, Decimal("0")) + batch["amount"]

        return sorted(totals.items())
