"""Night 6: read a CSV, use a list and dictionary, and run a function."""

import csv
from decimal import Decimal
from pathlib import Path


def calculate_net_revenue(transaction):
    interchange = Decimal(transaction["interchange_amount"])
    rebate = Decimal(transaction["rebate_amount"])
    return interchange - rebate


csv_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "synthetic"
    / "transactions.csv"
)

with csv_path.open(newline="", encoding="utf-8") as csv_file:
    transactions = list(csv.DictReader(csv_file))

first_transaction = transactions[0]
net_revenue = calculate_net_revenue(first_transaction)

print(f"Transactions loaded: {len(transactions)}")
print(f"Customer ID: {first_transaction['customer_id']}")
print(f"Customer: {first_transaction['customer_name']}")
print(f"Interchange: ${Decimal(first_transaction['interchange_amount']):,.2f}")
print(f"Rebate: ${Decimal(first_transaction['rebate_amount']):,.2f}")
print(f"Calculated net revenue: ${net_revenue:,.2f}")
print(f"Recorded CSV revenue: ${Decimal(first_transaction['revenue_amount']):,.2f}")
