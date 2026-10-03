"""Regression suite: run before a release (shape C's release flow, `verify-regression`)."""

from stockroom.core import Item, add_item, remove_item, total_value


def test_round_trip_leaves_stock_empty():
    stock = {}
    for n in range(50):
        stock = add_item(stock, Item(f"S{n}", n + 1, 0.99))
    for n in range(50):
        stock = remove_item(stock, f"S{n}", n + 1)
    assert stock == {}


def test_value_is_stable_to_pence():
    stock = add_item({}, Item("P", 3, 0.1))
    assert total_value(stock) == 0.3
