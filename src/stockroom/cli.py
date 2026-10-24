"""The ``stockroom`` command line."""

from __future__ import annotations

import argparse
import csv
import sys
from typing import TextIO

from stockroom.core import Item, add_item

REPORT_FORMATS = ("csv",)
REPORT_FIELDS = ("sku", "quantity", "unit_price", "value")


def read_stock(source: TextIO) -> dict[str, Item]:
    """Read a stock from CSV with the columns ``sku``, ``quantity`` and ``unit_price``."""
    stock: dict[str, Item] = {}
    for row in csv.DictReader(source):
        stock = add_item(stock, Item(row["sku"], int(row["quantity"]), float(row["unit_price"])))
    return stock


def write_report(stock: dict[str, Item], out: TextIO, fmt: str = "csv") -> None:
    """Write one row per SKU, sorted by SKU, in ``fmt``."""
    if fmt not in REPORT_FORMATS:
        raise ValueError(f"unsupported report format: {fmt}")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(REPORT_FIELDS)
    for sku in sorted(stock):
        item = stock[sku]
        writer.writerow([item.sku, item.quantity, item.unit_price, round(item.quantity * item.unit_price, 2)])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stockroom")
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="write a stock report")
    report.add_argument("stock", type=argparse.FileType("r"), help="stock CSV (sku,quantity,unit_price)")
    report.add_argument("--format", choices=REPORT_FORMATS, default="csv", help="output format; default csv")
    return parser


def main(argv: list[str] | None = None, out: TextIO | None = None) -> int:
    args = build_parser().parse_args(argv)
    with args.stock as source:
        stock = read_stock(source)
    write_report(stock, out or sys.stdout, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
