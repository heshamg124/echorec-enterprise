import pytest

from stockroom.core import Item, add_item, low_stock, remove_item, total_value


def test_add_merges_quantities():
    stock = add_item({}, Item("A1", 2, 1.5))
    stock = add_item(stock, Item("A1", 3, 1.5))
    assert stock["A1"].quantity == 5


def test_add_rejects_negative():
    with pytest.raises(ValueError):
        add_item({}, Item("A1", -1, 1.0))


def test_remove_drops_empty_sku():
    stock = add_item({}, Item("B2", 2, 4.0))
    assert remove_item(stock, "B2", 2) == {}


def test_remove_too_many():
    stock = add_item({}, Item("B2", 1, 4.0))
    with pytest.raises(ValueError):
        remove_item(stock, "B2", 2)


def test_total_value():
    stock = add_item(add_item({}, Item("A", 3, 0.1)), Item("B", 2, 2.25))
    assert total_value(stock) == 4.8


def test_low_stock():
    stock = add_item(add_item({}, Item("Z", 1, 1.0)), Item("A", 10, 1.0))
    assert low_stock(stock) == ["Z"]
