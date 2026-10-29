"""Verify the valid teaching dataset against its recorded financial controls.

These checks cover the CSV delivered for the starter project. They do not imply
that the future analytical agent or invalid-input evaluation fixtures exist.
Run from the repository root: python -m unittest discover -s tests -v
"""

import csv
from collections import Counter
from datetime import date
from decimal import Decimal, localcontext
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "synthetic" / "transactions.csv"
EXPECTED_PATH = ROOT / "docs" / "synthetic-expected-results.json"
D = Decimal
ZERO = D("0")
RATE_TOLERANCE = D("1e-24")
BPS_TOLERANCE = D("1e-20")

COLUMNS = [
    "business_line", "customer_name", "customer_id", "vendor_name",
    "spend_amount", "interchange_amount", "rebate_amount", "revenue_amount",
    "transaction_description", "client_segment", "settlement_date", "card_product", "mcc",
]
AMOUNT_FIELDS = (
    "spend_amount", "interchange_amount", "rebate_amount", "revenue_amount",
)
CUSTOMER_IDS = {"0001", "0002", "0003", "0004", "0005", "0006"}
PERIODS = ("2026-08", "2026-09")


def totals(rows):
    return {
        field: sum((D(row[field]) for row in rows), ZERO)
        for field in AMOUNT_FIELDS
    }


def rates(amounts):
    """Calculate rates using aggregate amounts, with extra comparison precision."""
    with localcontext() as context:
        context.prec = 40
        spend = amounts["spend_amount"]
        return {
            "gross_interchange_rate": amounts["interchange_amount"] / spend,
            "rebate_rate": amounts["rebate_amount"] / spend,
            "net_revenue_yield": amounts["revenue_amount"] / spend,
        }


class SyntheticDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            cls.columns = reader.fieldnames
            cls.rows = list(reader)
        cls.document = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        cls.expected = cls.document["expected"]

    def rows_for(self, period, customer_id=None):
        return [
            row for row in self.rows
            if row["settlement_date"].startswith(period)
            and (customer_id is None or row["customer_id"] == customer_id)
        ]

    def assert_amounts_match(self, actual, expected):
        for field in AMOUNT_FIELDS:
            with self.subTest(field=field):
                self.assertEqual(actual[field], D(expected[field]))

    def assert_rates_match(self, actual, expected):
        for field in ("gross_interchange_rate", "rebate_rate", "net_revenue_yield"):
            with self.subTest(rate=field):
                self.assertLessEqual(abs(actual[field] - D(expected[field])), RATE_TOLERANCE)
        self.assertLessEqual(
            abs(actual["gross_interchange_rate"] - actual["rebate_rate"] - actual["net_revenue_yield"]),
            RATE_TOLERANCE,
        )

    def test_exact_ordered_columns_and_required_values(self):
        self.assertEqual(self.columns, COLUMNS)
        self.assertEqual(self.document["columns"], COLUMNS)
        for index, row in enumerate(self.rows, start=2):
            with self.subTest(csv_line=index):
                self.assertEqual(list(row), COLUMNS)
                self.assertTrue(all(value is not None and value != "" for value in row.values()))

    def test_row_counts_periods_and_customer_coverage(self):
        self.assertEqual(len(self.rows), 50)
        self.assertEqual(self.document["row_count"], 50)
        self.assertEqual({row["settlement_date"][:7] for row in self.rows}, set(PERIODS))
        for period in PERIODS:
            with self.subTest(period=period):
                selected = self.rows_for(period)
                self.assertEqual(len(selected), 25)
                self.assertEqual(len(selected), self.expected["monthly"][period]["row_count"])
                self.assertEqual({row["customer_id"] for row in selected}, CUSTOMER_IDS)
                category_counts = Counter(row["transaction_description"] for row in selected)
                self.assertEqual(category_counts, {"Standard": 12, "Premium": 12, "Refund": 1})
                for customer_id in CUSTOMER_IDS:
                    regular_categories = Counter(
                        row["transaction_description"]
                        for row in selected
                        if row["customer_id"] == customer_id and row["transaction_description"] != "Refund"
                    )
                    self.assertEqual(regular_categories, {"Standard": 2, "Premium": 2})

    def test_declared_full_month_coverage_and_valid_settlement_dates(self):
        boundaries = {
            "2026-08": ("2026-08-01", "2026-08-31"),
            "2026-09": ("2026-09-01", "2026-09-30"),
        }
        for period, (start, end) in boundaries.items():
            with self.subTest(period=period):
                coverage = self.document["periods"][period]
                self.assertIs(coverage["complete"], True)
                self.assertEqual((coverage["coverage_start"], coverage["coverage_end"]), (start, end))
                self.assertEqual(coverage["expected_rows"], len(self.rows_for(period)))
                for row in self.rows_for(period):
                    settled = date.fromisoformat(row["settlement_date"])
                    self.assertLessEqual(date.fromisoformat(start), settled)
                    self.assertLessEqual(settled, date.fromisoformat(end))

    def test_money_precision_and_each_row_reconciles(self):
        for index, row in enumerate(self.rows, start=2):
            with self.subTest(csv_line=index):
                for field in AMOUNT_FIELDS:
                    self.assertRegex(row[field], r"^-?\d+\.\d{2}$")
                    self.assertEqual(D(row[field]).as_tuple().exponent, -2)
                self.assertEqual(
                    D(row["revenue_amount"]),
                    D(row["interchange_amount"]) - D(row["rebate_amount"]),
                )

    def test_ids_and_illustrative_mcc_labels_keep_leading_zeroes(self):
        self.assertEqual({row["customer_id"] for row in self.rows}, CUSTOMER_IDS)
        self.assertEqual({row["mcc"] for row in self.rows}, {"0011", "0022"})
        for row in self.rows:
            with self.subTest(customer=row["customer_id"], date=row["settlement_date"]):
                self.assertIsInstance(row["customer_id"], str)
                self.assertIsInstance(row["mcc"], str)
                self.assertRegex(row["customer_id"], r"^000[1-6]$")
                self.assertRegex(row["mcc"], r"^00[12][12]$")

    def test_names_and_category_attributes_are_consistent(self):
        category_attributes = {
            "Standard": ("Demo Paper Kite Supply", "Virtual", "0011"),
            "Premium": ("Demo Silver Compass Services", "Plastic", "0022"),
            "Refund": ("Demo Paper Kite Supply", "Virtual", "0011"),
        }
        for customer_id in CUSTOMER_IDS:
            selected = [row for row in self.rows if row["customer_id"] == customer_id]
            self.assertEqual(
                {row["customer_name"] for row in selected},
                {self.expected["customers"][customer_id]["customer_name"]},
            )
            self.assertEqual(len({row["client_segment"] for row in selected}), 1)
            self.assertEqual({row["business_line"] for row in selected}, {"Fictional Commercial Payments"})
        for row in self.rows:
            self.assertEqual(
                (row["vendor_name"], row["card_product"], row["mcc"]),
                category_attributes[row["transaction_description"]],
            )

    def test_monthly_control_totals_and_aggregate_rate_identity(self):
        for period in PERIODS:
            with self.subTest(period=period):
                actual = totals(self.rows_for(period))
                expected = self.expected["monthly"][period]
                self.assert_amounts_match(actual, expected)
                self.assert_rates_match(rates(actual), expected)

    def test_customer_controls_and_yield_changes(self):
        for customer_id in CUSTOMER_IDS:
            with self.subTest(customer=customer_id):
                customer_expected = self.expected["customers"][customer_id]
                observed = {}
                for period in PERIODS:
                    amounts = totals(self.rows_for(period, customer_id))
                    observed[period] = amounts
                    expected = customer_expected["periods"][period]
                    self.assert_amounts_match(amounts, expected)
                    self.assert_rates_match(rates(amounts), expected)
                self.assertEqual(
                    observed["2026-09"]["spend_amount"] - observed["2026-08"]["spend_amount"],
                    D(customer_expected["spend_variance"]),
                )
                self.assertEqual(
                    observed["2026-09"]["revenue_amount"] - observed["2026-08"]["revenue_amount"],
                    D(customer_expected["net_revenue_variance"]),
                )
                bps_change = D(10000) * (
                    rates(observed["2026-09"])["net_revenue_yield"]
                    - rates(observed["2026-08"])["net_revenue_yield"]
                )
                self.assertLessEqual(
                    abs(bps_change - D(customer_expected["net_revenue_yield_change_bps"])),
                    BPS_TOLERANCE,
                )

    def test_customer_dollar_changes_reconcile_to_overall_variance(self):
        changes = {
            customer_id: totals(self.rows_for("2026-09", customer_id))["revenue_amount"]
            - totals(self.rows_for("2026-08", customer_id))["revenue_amount"]
            for customer_id in CUSTOMER_IDS
        }
        overall = totals(self.rows_for("2026-09"))["revenue_amount"] - totals(self.rows_for("2026-08"))["revenue_amount"]
        self.assertEqual(sum(changes.values(), ZERO), overall)
        self.assertEqual(overall, D("-1898.00"))
        self.assertEqual(overall, D(self.expected["month_over_month"]["net_revenue_variance"]))
        self.assertEqual(max(changes, key=lambda key: abs(changes[key])), "0002")
        self.assertEqual(changes["0002"], D("-1750.00"))

    def test_refunds_are_signed_full_reversals_of_earlier_purchases(self):
        refunds = [row for row in self.rows if row["transaction_description"] == "Refund"]
        self.assertEqual(len(refunds), 2)
        for refund in refunds:
            with self.subTest(period=refund["settlement_date"][:7]):
                self.assertTrue(all(D(refund[field]) < ZERO for field in AMOUNT_FIELDS))
                matching_purchases = [
                    row for row in self.rows
                    if row["transaction_description"] == "Standard"
                    and row["settlement_date"][:7] == refund["settlement_date"][:7]
                    and row["settlement_date"] < refund["settlement_date"]
                    and all(row[field] == refund[field] for field in (
                        "customer_id", "customer_name", "vendor_name", "card_product", "mcc",
                    ))
                    and all(D(row[field]) == -D(refund[field]) for field in AMOUNT_FIELDS)
                ]
                self.assertTrue(matching_purchases, "Refund must reverse a matching earlier positive purchase.")
                self.assertEqual(D(refund["revenue_amount"]), D("-15.00"))

    def test_small_negative_yield_customer_has_positive_spend_in_both_periods(self):
        prior = totals(self.rows_for("2026-08", "0006"))
        current = totals(self.rows_for("2026-09", "0006"))
        self.assertEqual(prior["spend_amount"], D("400.00"))
        self.assertEqual(current["spend_amount"], D("400.00"))
        self.assertEqual(current["revenue_amount"], D("-1.00"))
        self.assertEqual(rates(current)["net_revenue_yield"], D("-0.0025"))
        self.assertEqual(
            D(10000) * (rates(current)["net_revenue_yield"] - rates(prior)["net_revenue_yield"]),
            D("-200"),
        )

    def test_first_row_matches_the_night_six_example(self):
        first = self.rows[0]
        self.assertEqual(first["customer_id"], "0001")
        self.assertEqual(D(first["spend_amount"]), D("1000.00"))
        self.assertEqual(D(first["interchange_amount"]), D("25.00"))
        self.assertEqual(D(first["rebate_amount"]), D("10.00"))
        self.assertEqual(D(first["revenue_amount"]), D("15.00"))
        self.assertEqual(D(first["interchange_amount"]) - D(first["rebate_amount"]), D("15.00"))


if __name__ == "__main__":
    unittest.main()
