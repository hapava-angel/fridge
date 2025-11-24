from decimal import Decimal
from main import Frige
from pprint import pprint

frige_items = {}

Frige.add(frige_items, "Молоко", Decimal("1"), "2025-03-01")
Frige.add(frige_items, "Творог 9%", Decimal("0.4"), "2025-02-27")
Frige.add_by_note(frige_items, "Сметана 0.2 2025-02-25")
Frige.add(frige_items, "Курица филе", Decimal("1.2"), "2025-02-28")
Frige.add_by_note(frige_items, "Говядина 0.8 2025-03-10")
Frige.add_by_note(frige_items, "Сёмга стейки 0.5 2025-02-26")
Frige.add_by_note(frige_items, "Пельмени Сибирские 1.0 2026-01-01")
Frige.add(frige_items, "Овощная смесь", Decimal("0.7"))
Frige.add_by_note(frige_items, "Хлеб Бородинский 0.6 2025-02-24")
Frige.add(frige_items, "Булочки сливочные", Decimal("0.3"), "2025-02-23")
Frige.add(frige_items, "Помидоры", Decimal("0.5"), "2025-02-22")
Frige.add(frige_items, "Яблоки красные", Decimal("1.0"), "2025-03-05")
Frige.add_by_note(frige_items, "Кетчуп 0.4 2025-12-01")
Frige.add_by_note(frige_items, "Соевый соус 0.25")
Frige.add(frige_items, "Вода питьевая", Decimal("2"))
Frige.add(frige_items, "Сок апельсиновый", Decimal("1.0"), "2025-03-15")


print("Холодильник заполнен:")
pprint(frige_items, width=80, sort_dicts=False)
