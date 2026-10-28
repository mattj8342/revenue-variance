# Learning log

## 2026 10 27

Defined the Revenue Variance Investigation Agent as an investigation of period-over-period net revenue movement.

Chose three business questions covering spend volume, interchange mix and rebates, and the largest drivers. The driver question has separate dollar-impact and rate-movement views.

Outlined a workflow of business question, read-only tool use, deterministic calculations, anomaly checks, supporting explanation, and human review.

### Synthetic dataset decisions

- Use one row per fictional settled transaction and USD amounts.
- Derive reporting months from settlement date.
- Calculate net revenue as interchange minus customer rebate; net revenue is not profit.
- Use 13 generic columns in one table, with a single customer name/ID pair and a single standardized vendor name.
- Keep business lines, client segments, interchange categorizations, customer and vendor identities, and financial values fictional.
- Use generic card products such as plastic or virtual card and retain merchant category code.
- Give refunds their own invented categorization and a documented signed-amount convention.
- Include every comparable positive-spend group in rate rankings, with spend and dollar context and no default minimum-dollar cutoff.

The public specification is self-contained and does not depend on internal source mappings or a real-data extract.

Next: generate the fictional dataset and known expected answers, then implement the calculations and reusable analysis skills.

## Future entries

For each session, record the date, change, verification, lesson learned, blocker, and next step.
