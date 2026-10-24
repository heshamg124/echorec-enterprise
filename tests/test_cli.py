import csv
import io

import pytest

from stockroom.cli import main, write_inventory, write_summary


@pytest.fixture
def stock_file(tmp_path):
    path = tmp_path / "stock.csv"
    path.write_text("sku,quantity,unit_price\nB2,2,2.25\nA1,3,0.1\nA1,1,0.1\n")
    return str(path)


def test_report_format_csv(stock_file):
    out = io.StringIO()
    assert main(["report", stock_file, "--format", "csv"], out=out) == 0
    rows = list(csv.reader(io.StringIO(out.getvalue())))
    assert rows == [
        ["sku", "quantity", "unit_price", "value"],
        ["A1", "4", "0.1", "0.4"],
        ["B2", "2", "2.25", "4.5"],
    ]


def test_report_defaults_to_csv(stock_file):
    explicit, default = io.StringIO(), io.StringIO()
    main(["report", stock_file, "--format", "csv"], out=explicit)
    main(["report", stock_file], out=default)
    assert default.getvalue() == explicit.getvalue()


@pytest.mark.parametrize("fmt", ["json", "xlsx"])
def test_report_rejects_other_formats(stock_file, fmt, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["report", stock_file, "--format", fmt], out=io.StringIO())
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_summary_format_csv(stock_file):
    out = io.StringIO()
    assert main(["summary", stock_file, "--format", "csv"], out=out) == 0
    rows = list(csv.reader(io.StringIO(out.getvalue())))
    assert rows == [["skus", "units", "total_value"], ["2", "6", "4.9"]]


def test_summary_defaults_to_csv(stock_file):
    explicit, default = io.StringIO(), io.StringIO()
    main(["summary", stock_file, "--format", "csv"], out=explicit)
    main(["summary", stock_file], out=default)
    assert default.getvalue() == explicit.getvalue()


@pytest.mark.parametrize("fmt", ["json", "xlsx"])
def test_summary_rejects_other_formats(stock_file, fmt, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["summary", stock_file, "--format", fmt], out=io.StringIO())
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_write_summary_raises_for_unsupported_format():
    with pytest.raises(ValueError, match="unsupported summary format"):
        write_summary({}, io.StringIO(), "json")


def test_inventory_format_csv(stock_file):
    out = io.StringIO()
    assert main(["inventory", stock_file, "--format", "csv"], out=out) == 0
    rows = list(csv.reader(io.StringIO(out.getvalue())))
    assert rows == [["sku", "quantity"], ["A1", "4"], ["B2", "2"]]


def test_inventory_defaults_to_csv(stock_file):
    explicit, default = io.StringIO(), io.StringIO()
    main(["inventory", stock_file, "--format", "csv"], out=explicit)
    main(["inventory", stock_file], out=default)
    assert default.getvalue() == explicit.getvalue()


@pytest.mark.parametrize("fmt", ["json", "xlsx"])
def test_inventory_rejects_other_formats(stock_file, fmt, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["inventory", stock_file, "--format", fmt], out=io.StringIO())
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_write_inventory_raises_for_unsupported_format():
    with pytest.raises(ValueError, match="unsupported inventory format"):
        write_inventory({}, io.StringIO(), "json")
