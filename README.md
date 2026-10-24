# echorec-enterprise

**An Echorec sample repository for team shape C — regulated enterprise.** Echorec's acceptance suite
runs that shape's flows against this repository: its agents open pull requests here, CI checks
them, and a human code owner approves every merge.

The code is deliberately small: `stockroom`, a stock ledger in `src/stockroom/`.

## Commands

- tests: `pytest -q`
- lint: `ruff check . && ruff format --check .`
- security scan: `bandit -q -r src`
- regression: `pytest -q regression`

The same commands run in CI (workflow `ci`) and in Echorec's run sandbox, built from
`.echorec/Dockerfile` (non-root; `.devcontainer/devcontainer.json` uses the same file).

## `stockroom report`

`stockroom report STOCK [--format FORMAT]` reads a stock CSV with the columns `sku`, `quantity`
and `unit_price` and writes a report to standard output. Rows for the same SKU are merged: their
quantities are added and the last row's unit price is kept.

`--format` accepts one value:

- `csv` (the default): a header row `sku,quantity,unit_price,value`, then one row per SKU sorted
  by SKU, where `value` is `quantity × unit_price` rounded to two decimal places. The file opens
  directly in a spreadsheet.

Any other value is rejected with an `invalid choice` error and exit status 2.

```console
$ stockroom report stock.csv --format csv > report.csv
$ cat report.csv
sku,quantity,unit_price,value
A1,4,0.1,0.4
B2,2,2.25,4.5
```

## `stockroom summary`

`stockroom summary STOCK [--format FORMAT]` reads the same stock CSV as `stockroom report`, merging
rows for the same SKU in the same way, and writes the stock totals to standard output.

`--format` accepts one value:

- `csv` (the default): a header row `skus,units,total_value`, then one row where `skus` is the
  number of distinct SKUs, `units` is the total quantity across all SKUs, and `total_value` is the
  sum of `quantity × unit_price` rounded to two decimal places. The file opens directly in a
  spreadsheet.

Any other value is rejected with an `invalid choice` error and exit status 2.

```console
$ stockroom summary stock.csv --format csv > summary.csv
$ cat summary.csv
skus,units,total_value
2,6,4.9
```

## `stockroom inventory`

`stockroom inventory STOCK [--format FORMAT]` reads the same stock CSV as `stockroom report`,
merging rows for the same SKU in the same way, and writes the quantity on hand of each SKU to
standard output.

`--format` accepts one value:

- `csv` (the default): a header row `sku,quantity`, then one row per SKU sorted by SKU. The file
  opens directly in a spreadsheet.

Any other value is rejected with an `invalid choice` error and exit status 2.

```console
$ stockroom inventory stock.csv --format csv > inventory.csv
$ cat inventory.csv
sku,quantity
A1,4
B2,2
```

## Rules

- `main` is protected: a pull request, one approving review from a code owner, and passing
  `ci` checks. No force pushes.
- Nothing here is secret, and nothing secret may be added.
