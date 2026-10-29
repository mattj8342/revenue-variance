# Revenue Variance Investigation Agent

An analytics project that investigates why net revenue changed between comparable periods and identifies where an analyst should look first.

The planned agent will examine settled spend, interchange mix, customer rebates, and net revenue yield. It will explain the largest changes in both dollars and rates, show supporting metrics, and suggest follow-up questions for human review.

**Status:** A reviewed fictional transaction CSV, known expected results, dataset checks, and the first Python exercise are available. The investigation agent and full analytical tools have not been implemented yet.

## Start with the data and Night 6

Use [the synthetic transaction CSV](data/synthetic/transactions.csv) for both the project and the beginner exercise. It contains 50 fictional rows across August and September 2026, with the thirteen documented columns.

Follow [Night 6 in GitHub Codespaces](docs/night-06-codespaces.md) to read the CSV into a list of dictionaries, calculate one transaction's net revenue, and change a small Python function. The repository files are already present in a codespace; no CSV upload is needed.

From the repository root:

```bash
python3 lessons/night_06.py
```

The original first-row result is **25.00 interchange - 10.00 rebate = 15.00 net revenue**. [Dataset notes and monthly controls](data/synthetic/README.md) explain the designed patterns. The [expected-results record](docs/synthetic-expected-results.json) supplies known amounts for later analytical checks.

## Business questions

1. **Has spend increased or decreased compared with the prior comparable period?** Measure the dollar and percentage change overall and by customer.
2. **How have interchange mix and customer rebates affected the blended gross interchange rate and net revenue yield?** Distinguish changes in the spend mix from rate changes within categories.
3. **Which customers, vendors, or interchange categories show the largest changes in net revenue dollars and net revenue yield?** Provide separate dollar-impact and rate-movement rankings, with spend context and suggested follow-up questions.

See [Business questions and analysis rules](docs/business-questions.md) for the detailed scope.

## Planned workflow

1. Receive the business question and identify the comparison periods.
2. Validate the synthetic dataset and metric definitions.
3. Retrieve the required current and prior-period data through read-only analytical tools.
4. Calculate changes using deterministic queries or functions, then break results down by customer, standardized vendor name, interchange categorization, business line, client segment, card product, or MCC.
5. Flag the largest drivers and data-quality anomalies.
6. Return a short explanation with supporting metrics, calculation references, limitations, and recommended follow-up questions.
7. Require human review before a business decision or distribution of findings.

The first demo uses local synthetic data. SQL or Power BI tools may be added later. The language model will select analytical steps and explain results; queries and functions will calculate the metrics.

## Measures

| Measure | Definition |
| --- | --- |
| Spend variance | Current spend minus prior spend |
| Net revenue | Gross interchange dollars minus customer rebate dollars; not profit |
| Net revenue variance | Current net revenue minus prior net revenue |
| Net revenue yield | Total net revenue divided by total settled spend |
| Blended gross interchange rate | Total interchange dollars divided by total settled spend |
| Rebate rate | Total rebate dollars divided by total settled spend |
| Rate change in basis points | 10,000 times the change in a rate stored as a decimal |

Rates come from aggregated amounts, rather than an average of transaction rates. For the same population and spend denominator, net revenue yield equals gross interchange rate minus rebate rate.

Rate rankings include all comparable groups with valid positive spend by default, with no minimum-dollar cutoff. Show spend beside basis-point movement so smaller customers remain visible in context.

## Synthetic dataset

The dataset has **13 generic columns**, with one row per fictional settled transaction. It uses USD, settlement-date reporting, complete comparison periods, consistent customer/category representation, and a distinct refund categorization.

All customer names, IDs, vendor names, categories, amounts, and rates in the starter dataset are invented. The current specification uses generic fields without internal source mappings. See the [synthetic data requirements](docs/data-contract.md) and [data folder notes](data/synthetic/README.md).

## Repository contents

```text
README.md
.gitignore
docs/
  business-questions.md
  data-contract.md
  learning-log.md
  night-06-codespaces.md
  synthetic-expected-results.json
data/
  synthetic/
    README.md
    transactions.csv
lessons/
  night_06.py
tests/
  test_synthetic_data.py
```

The `.gitignore` excludes common raw exports, private data folders, credentials, and generated outputs. Reviewed synthetic CSV files in `data/synthetic/` are allowed through the CSV rules. Ignore rules do not inspect file contents, protect access, or remove earlier commits.

## Next milestones

- Complete the Night 6 exercise personally: run, modify, and explain the Python function.
- Add separately labeled fault fixtures for the remaining evaluation scenarios.
- Implement and verify the analytical calculations.
- Write reusable analysis skills for validation, period comparison, mix investigation, driver ranking, and evidence-based explanations.
- Connect those skills to read-only tools and evaluate the question-to-answer workflow.

Validate the starter dataset with `python3 -m unittest discover -s tests -v`. The project is still in progress; this first exercise does not implement the investigation agent.

Progress and decisions are recorded in the [learning log](docs/learning-log.md).

## Initial scope

Compare two completed settlement-month periods in USD using net revenue. Keep forecasting, write access to data sources, automatic distribution, and business actions outside the first version.
