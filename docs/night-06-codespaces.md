# Night 6: read the project CSV and change a Python function

Use the same fictional transaction data that will support the Revenue Variance Investigation Agent. This first exercise reads one transaction and calculates its net revenue. It does not build the agent yet.

Allow about 30–45 minutes. No extra Python packages or model API keys are needed.

## 1. Open the correct branch in Codespaces

1. Sign in to your personal GitHub account and open [the starter branch](https://github.com/mattj8342/revenue-variance/tree/codex/synthetic-data-night-6).
2. Confirm the branch selector says `codex/synthetic-data-night-6`. If these files have since been merged, use `main` instead.
3. Click **Code**, then **Codespaces**, then the option to create a codespace for the selected branch.
4. Review who pays for the codespace. The default small machine is sufficient for this exercise.
5. Wait for the browser editor to open. In the file explorer, check that you can see `data/synthetic/transactions.csv` and `lessons/night_06.py`.

The repository is cloned into the codespace, so the CSV is already there. Do not upload another copy.

GitHub documents the [repository and branch creation steps](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository). Its [default environment includes Python](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers#using-the-default-dev-container-configuration).

## 2. Open a terminal and check Python

Use the editor's **Terminal → New Terminal** menu. In the terminal, run:

```bash
python3 --version
```

The result should begin with `Python 3`. Then open `lessons/night_06.py` in the editor and run:

```bash
python3 lessons/night_06.py
```

Expected output:

```text
Transactions loaded: 50
Customer ID: 0001
Customer: Demo Cedar Lantern Studio
Interchange: $25.00
Rebate: $10.00
Calculated net revenue: $15.00
Recorded CSV revenue: $15.00
```

If Python cannot find the script, check that the terminal is in the repository root. If the CSV or lesson is missing, check the branch selected in Step 1. Do not install packages to fix a missing-file error.

## 3. Identify the list, dictionary, and function

This line reads the CSV:

```python
transactions = list(csv.DictReader(csv_file))
```

- The CSV header supplies the dictionary keys: `customer_id`, `interchange_amount`, and the other column names.
- Each CSV row becomes a **dictionary**, like a record with named fields.
- `transactions` is a **list** holding all fifty dictionaries.
- `transactions[0]` selects the first row. Python starts list positions at zero.
- `first_transaction["interchange_amount"]` selects the interchange field from that row.

This is the function:

```python
def calculate_net_revenue(transaction):
    interchange = Decimal(transaction["interchange_amount"])
    rebate = Decimal(transaction["rebate_amount"])
    return interchange - rebate
```

`def` defines a reusable function. Its input is one transaction dictionary. `return` sends the answer back to the calling line. `Decimal` converts CSV text such as `"25.00"` into an exact decimal amount for money.

For the first row, the function returns 25.00 minus 10.00, which is 15.00. This matches the CSV's recorded revenue.

## 4. Change the function and predict the result

Try a what-if calculation that adds five dollars to the rebate. Keep the saved dataset unchanged so its expected results remain useful.

Replace the function with:

```python
def calculate_net_revenue(transaction, extra_rebate="0.00"):
    interchange = Decimal(transaction["interchange_amount"])
    rebate = Decimal(transaction["rebate_amount"])
    return interchange - rebate - Decimal(extra_rebate)
```

Then change this calling line:

```python
net_revenue = calculate_net_revenue(first_transaction)
```

to:

```python
net_revenue = calculate_net_revenue(first_transaction, extra_rebate="5.00")
```

Before running it, predict the result. Save the script with **Ctrl+S**, then rerun:

```bash
python3 lessons/night_06.py
```

The calculated net revenue should now be **$10.00**. The CSV's rebate line still shows its original $10.00, and its recorded revenue still shows $15.00. The extra $5.00 exists only in this what-if function call; the script never writes to the CSV.

Change `"5.00"` to `"2.50"` and predict the next calculated result: **$12.50**. A call without the new argument uses the default extra rebate of zero.

## 5. Inspect another row and explain one error

Change:

```python
first_transaction = transactions[0]
```

to:

```python
first_transaction = transactions[2]
```

This selects the third transaction. With no extra rebate, its net revenue is $30.00 minus $10.00 = **$20.00**. Set the extra rebate back to zero before checking that result.

For an error exercise, temporarily change the function's dictionary key from `"interchange_amount"` to `"interchange_amount_typo"`. Running it raises `KeyError`: the dictionary has no field with that exact name. Read the error, correct the key, and rerun successfully.

At the end, choose whether your committed lesson should show the original calculation or a clearly explained what-if example. Keep the canonical CSV unchanged.

## 6. Save your learning evidence

Record these in your learning log:

- The command you ran.
- The original result and the result after your change.
- What the list holds, what one dictionary represents, and what the function returns.
- The error you introduced and how you fixed it.

You can save your own script changes from Codespaces with:

```bash
git add lessons/night_06.py
git commit -m "Practice CSV dictionaries and a net revenue function"
git push
```

Only commit when you have a change you want to keep. If Git says there is nothing to commit, the saved file may already match the branch. Mark Night 6 complete after you personally run, modify, and explain the exercise.

When finished, use **Ctrl+Shift+P → Codespaces: Stop Codespace**, or visit [Your Codespaces](https://github.com/codespaces), open its **…** menu, and select **Stop codespace**. Closing the browser tab alone does not stop it. [GitHub stop/start instructions](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace)

## Data and project references

- [Synthetic transactions](../data/synthetic/transactions.csv)
- [Dataset explanation](../data/synthetic/README.md)
- [Known expected results](synthetic-expected-results.json)
- [Business questions](business-questions.md)
- [Data contract](data-contract.md)

The main CSV contains valid starter data. Missing-field, incomplete-period, inconsistent-revenue, and zero-denominator fault cases will be separate evaluation fixtures later; they are not silently inserted into this dataset.
