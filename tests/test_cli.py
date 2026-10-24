import csv
import io

import pytest

from stockroom.cli import main


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
