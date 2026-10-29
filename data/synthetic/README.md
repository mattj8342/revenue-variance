# Synthetic transaction data

[transactions.csv](transactions.csv) contains **50 wholly fictional settled transactions** with the exact thirteen columns in the [data contract](../../docs/data-contract.md).

- Periods: August and September 2026, declared complete synthetic comparison months.
- Six fictional customers, with the same IDs and names in each month.
- Twenty-five rows per month: twenty-four purchases and one signed refund.
- USD amounts stored to two decimal places. Net revenue equals interchange minus rebate.
- Customer IDs and MCC labels are text values with leading zeros.
- All names, labels, amounts, and rates were invented for this project. No real records, internal source mappings, or identity crosswalks were used.

"Complete" describes the full set of transactions designed for each comparison month. It does not mean there is a transaction on every calendar date. Deliberately incomplete periods belong in separate fault fixtures.

## Fictional labels

`Standard` and `Premium` are invented interchange categories, not actual network pricing categories. `Refund` marks a signed full reversal of a Standard purchase. The MCC values `0011` and `0022` are deliberately illustrative invented labels, not claims about actual merchant-category classifications.

## Controlled examples

| Customer ID | Fictional customer | Designed pattern |
| --- | --- | --- |
| 0001 | Demo Cedar Lantern Studio | Stable purchases with an equal full refund in each period |
| 0002 | Demo Granite Harbor Works | Spend falls while mix and rates stay steady |
| 0003 | Demo Maple Orbit Supply | Spend stays steady and shifts toward the lower-yield category |
| 0004 | Demo Blue Finch Services | Spend and mix stay steady while gross interchange rates decline |
| 0005 | Demo Amber Bridge Goods | Spend, gross rates, and mix stay steady while rebates increase |
| 0006 | Demo Tiny Comet Shop | Small positive spend with a large yield decline and negative current net revenue |

These deliberately small examples make it easier to check calculations and distinguish dollar impact from rate movement. Customer, vendor, and category views describe the same underlying dollars.

## Known monthly amounts

| Month | Settled spend | Gross interchange | Customer rebate | Net revenue |
| --- | ---: | ---: | ---: | ---: |
| August 2026 | 443,400.00 | 12,221.00 | 4,434.00 | 7,787.00 |
| September 2026 | 343,400.00 | 9,365.00 | 3,476.00 | 5,889.00 |
| September minus August | -100,000.00 | -2,856.00 | -958.00 | -1,898.00 |

See [the expected-results record](../../docs/synthetic-expected-results.json) for customer controls, aggregate rates, category definitions, and scenario limitations. These are designed synthetic controls, not measured business results.

The first row has 1,000.00 spend, 25.00 interchange, 10.00 rebate, and 15.00 net revenue. Use it for [Night 6 in Codespaces](../../docs/night-06-codespaces.md). That exercise reads the same file the later project will use.

## Validate the saved CSV

From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The checks cover the schema, data identities, cent-level arithmetic, period/customer controls, signed refunds, and known expected results.

Keep this base dataset valid. Add malformed inputs, zero-spend denominators, and incomplete-period cases as separately labeled test fixtures during the evaluation phase. The current CSV does not cover every fault scenario in the data contract.

The ignore rules allow reviewed CSV files in this folder. They do not inspect file contents.
