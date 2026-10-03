"""A tiny stock ledger: the code Echorec's agents change in this sample repository."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    sku: str
    quantity: int
    unit_price: float


def add_item(stock: dict[str, Item], item: Item) -> dict[str, Item]:
    """Return a new stock with ``item`` added, merging quantities for an existing SKU."""
    if item.quantity < 0:
        raise ValueError("quantity must not be negative")
    current = stock.get(item.sku)
    merged = item if current is None else Item(item.sku, current.quantity + item.quantity, item.unit_price)
    return {**stock, item.sku: merged}


def remove_item(stock: dict[str, Item], sku: str, quantity: int) -> dict[str, Item]:
    """Return a new stock with ``quantity`` units of ``sku`` taken out."""
    current = stock.get(sku)
    if current is None:
        raise KeyError(sku)
    if quantity > current.quantity:
        raise ValueError(f"only {current.quantity} of {sku} in stock")
    remaining = current.quantity - quantity
    rest = {k: v for k, v in stock.items() if k != sku}
    if remaining:
        rest[sku] = Item(sku, remaining, current.unit_price)
    return rest


def total_value(stock: dict[str, Item]) -> float:
    """The value of everything in stock, rounded to pence."""
    return round(sum(i.quantity * i.unit_price for i in stock.values()), 2)


def low_stock(stock: dict[str, Item], threshold: int = 5) -> list[str]:
    """SKUs at or below ``threshold`` units, sorted."""
    return sorted(i.sku for i in stock.values() if i.quantity <= threshold)
