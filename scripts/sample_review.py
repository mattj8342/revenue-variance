"""Review the two months in the synthetic revenue variance dataset.

Run from the repository root with python scripts/sample_review.py.
"""

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "synthetic" / "transactions.csv"
CONTROLS_PATH = ROOT / "docs" / "synthetic-expected-results.json"
AMOUNT_FIELDS = ("spend_amount", "interchange_amount", "rebate_amount", "revenue_amount")


@dataclass
class Totals:
    spend: Decimal = Decimal(0)
    interchange: Decimal = Decimal(0)
    rebate: Decimal = Decimal(0)

    @property
    def revenue(self):
        return self.interchange - self.rebate

    @property
    def yield_rate(self):
        return self.revenue / self.spend if self.spend > 0 else None

    def add(self, spend, interchange, rebate):
        self.spend += spend
        self.interchange += interchange
        self.rebate += rebate


def read_dataset(periods, columns):
    monthly = defaultdict(Totals)
    groups = {name: defaultdict(Totals) for name in ("Customer", "Vendor", "Category")}
    row_counts = Counter()
    customer_names = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != columns:
            raise ValueError("CSV columns do not match the synthetic data contract.")
        for row in reader:
            if None in row or any(not row[field] or not row[field].strip() for field in columns):
                raise ValueError(f"Line {reader.line_num} has missing or extra values.")
            try:
                period = date.fromisoformat(row["settlement_date"]).isoformat()[:7]
                amounts = [Decimal(row[field]) for field in AMOUNT_FIELDS]
            except (ValueError, InvalidOperation) as error:
                raise ValueError(f"Line {reader.line_num} has an invalid date or amount.") from error
            if any(not amount.is_finite() or amount.as_tuple().exponent != -2 for amount in amounts):
                raise ValueError(f"Line {reader.line_num} requires finite, two-decimal amounts.")
            spend, interchange, rebate, revenue = amounts
            if interchange - rebate != revenue:
                raise ValueError(f"Line {reader.line_num} does not reconcile to net revenue.")
            customer_id = row["customer_id"]
            customer = row["customer_name"]
            if customer_names.setdefault(customer_id, customer) != customer:
                raise ValueError(f"Customer {customer_id} has inconsistent names.")
            row_counts[period] += 1
            monthly[period].add(spend, interchange, rebate)
            groups["Customer"][period, f"{customer_id} {customer}"].add(spend, interchange, rebate)
            groups["Vendor"][period, row["vendor_name"]].add(spend, interchange, rebate)
            groups["Category"][period, row["transaction_description"]].add(spend, interchange, rebate)

    expected_counts = {period: details["expected_rows"] for period, details in periods.items()}
    if row_counts != expected_counts:
        raise ValueError(f"Expected monthly row counts {expected_counts}; found {dict(row_counts)}.")
    return monthly, groups


def money(amount, signed=False):
    sign = "-" if amount < 0 else "+" if signed else ""
    return f"{sign}${abs(amount):,.2f}"


def rate_change(before, after):
    return (after - before) * 10_000


def print_rankings(label, totals, prior, current):
    names = sorted({name for _, name in totals})
    comparisons = [(name, totals.get((prior, name), Totals()),
                    totals.get((current, name), Totals())) for name in names]
    dollar_ranking = sorted(comparisons, key=lambda row: abs(row[2].revenue - row[1].revenue), reverse=True)
    print(f"\n{label} drivers by absolute net revenue change")
    for name, before, after in dollar_ranking:
        print(f"  {name}: {money(before.revenue)} -> {money(after.revenue)}"
              f" ({money(after.revenue - before.revenue, signed=True)})")

    comparable = [(name, before, after, rate_change(before.yield_rate, after.yield_rate))
                  for name, before, after in comparisons if before.spend > 0 and after.spend > 0]
    print(f"{label} drivers by absolute net yield change")
    for name, before, after, change in sorted(comparable, key=lambda row: abs(row[3]), reverse=True):
        print(f"  {name}: {before.yield_rate:.2%} -> {after.yield_rate:.2%} ({change:+.2f} bps)"
              f" | spend {money(before.spend)} -> {money(after.spend)}"
              f" | net revenue change {money(after.revenue - before.revenue, signed=True)}")
    for name, before, after in comparisons:
        if before.spend <= 0 or after.spend <= 0:
            print(f"  {name}: excluded from yield ranking (nonpositive spend in at least one period).")


def main():
    controls = json.loads(CONTROLS_PATH.read_text(encoding="utf-8"))
    periods = controls["periods"]
    prior, current = sorted(periods)
    monthly, groups = read_dataset(periods, controls["columns"])
    before, after = monthly[prior], monthly[current]
    if before.spend <= 0 or after.spend <= 0:
        raise ValueError("The monthly comparison requires positive signed spend in both months.")

    print(f"Synthetic revenue variance review | {current} vs {prior}")
    print(f"Source: {CSV_PATH.relative_to(ROOT)} | USD | Net revenue = interchange minus rebate")
    for label, first, second in (
        ("Settled spend", before.spend, after.spend),
        ("Gross interchange", before.interchange, after.interchange),
        ("Customer rebates", before.rebate, after.rebate),
        ("Net revenue", before.revenue, after.revenue),
    ):
        print(f"{label}: {money(first)} -> {money(second)} ({money(second - first, signed=True)})")
    print(f"Spend change: {(after.spend - before.spend) / before.spend:+.2%}")
    for label, first, second in (
        ("Gross interchange rate", before.interchange / before.spend, after.interchange / after.spend),
        ("Rebate rate", before.rebate / before.spend, after.rebate / after.spend),
        ("Net revenue yield", before.yield_rate, after.yield_rate),
    ):
        print(f"{label}: {first:.4%} -> {second:.4%} ({rate_change(first, second):+.2f} bps)")

    spend_effect = (after.spend - before.spend) * before.yield_rate
    yield_effect = after.spend * (after.yield_rate - before.yield_rate)
    print("\nNet revenue bridge")
    print(f"  Spend change at prior yield: {money(spend_effect, signed=True)}")
    print(f"  Blended yield change at current spend: {money(yield_effect, signed=True)}")

    categories = groups["Category"]
    print("\nCategory share of signed settled spend")
    for name in sorted({name for _, name in categories}):
        first = categories.get((prior, name), Totals()).spend / before.spend
        second = categories.get((current, name), Totals()).spend / after.spend
        print(f"  {name}: {first:.2%} -> {second:.2%} ({(second - first) * 100:+.2f} pp)")

    print("\nDriver views describe the same dollars and should be read independently.")
    for label, totals in groups.items():
        print_rankings(label, totals, prior, current)
    print("\nFollow-up: Check whether the top dollar driver's spend, mix, or rates changed.")
    print("Review status: Synthetic demo results for human review.")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Sample review failed: {error}") from error
