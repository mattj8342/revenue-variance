# Synthetic data

This folder is reserved for reviewed, wholly fictional CSV data. No dataset has been added yet.

Use the 13 generic columns in the [data requirements](../../docs/data-contract.md). Each row represents one invented settled transaction in USD. Keep fictional customer IDs, names, standardized vendor names, and category labels consistent across periods.

Calculate net revenue as interchange minus rebate. Use settlement date for reporting periods and a distinct fictional refund categorization with consistent signed amounts.

Generate known expected results for the documented scenarios so both the calculations and agent explanations can be checked. No real-source mappings or real-to-fictional identity crosswalks belong in the public dataset.

The ignore rules allow CSV files in this folder. That is a file-location convention rather than a content check; review files before staging them.
