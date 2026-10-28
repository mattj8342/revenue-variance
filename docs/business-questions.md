# Business questions and analysis rules

## Overall purpose

Explain why net revenue changed between comparable settlement periods and identify the most useful next investigation. Net revenue is interchange minus customer rebate; it is not profit. Distinguish observed calculations from unconfirmed explanations.

The first dataset is entirely fictional. Each row represents one settled transaction, all financial amounts are USD, and reporting months come from `settlement_date`. Use complete comparison periods with customers and categories represented consistently.

## Question 1 Spend volume

**Has spend increased or decreased compared with the prior comparable period?**

Return current spend, prior spend, dollar variance, and percentage variance overall and by customer. Show whether the movement is concentrated in a few customers or spread across the population.

When prior spend is zero, percentage change is undefined. An unexpected missing customer or category in a deliberately complete demo period is a data-quality exception before it is evidence of changed activity.

## Question 2 Interchange mix and net revenue yield

**How have interchange mix and customer rebates affected the blended gross interchange rate and net revenue yield?**

Use `transaction_description` as the interchange categorization. Additional views can use card product, MCC, business line, or client segment. Return category spend shares, their changes, gross interchange rate, rebate rate, and net revenue yield for both periods.

```text
revenue_amount = interchange_amount - rebate_amount
net_revenue_yield = SUM(revenue_amount) / SUM(spend_amount)
gross_interchange_rate = SUM(interchange_amount) / SUM(spend_amount)
rebate_rate = SUM(rebate_amount) / SUM(spend_amount)
rate_change_bps = 10000 * (current_rate - prior_rate)
```

A change from 2.00% to 1.80% is a decrease of 20 basis points. Net revenue yield equals gross interchange rate minus rebate rate when calculated on the same population and spend denominator. Higher rebate rates can reduce net yield while spend mix and gross rates stay steady.

A future volume/mix/rate bridge must use one documented method and reconcile to the observed revenue-dollar change. Avoid overlapping explanations. Categories without a prior rate need explicit treatment rather than an invented baseline.

## Question 3 Drivers in dollars and rates

**Which customers, vendors, or interchange categories show the largest changes in net revenue dollars and net revenue yield?**

Produce two views for each dimension:

| View | Required output |
| --- | --- |
| Dollar impact | Current and prior net revenue, dollar variance, and contribution to the overall variance when meaningful |
| Rate movement | Current and prior net revenue yield, basis-point change, gross interchange and rebate rates, and both periods' spend |

Include increases and decreases. A large customer can dominate dollar variance while a small customer has a larger rate movement. Include all groups with valid positive spend in both periods, with **no minimum-dollar cutoff**. Show spend and dollar impact beside rate movement.

Use `customer_id` and `customer_name` for the customer view and the single standardized `vendor_name` for the vendor view. Customer, vendor, and category rankings are alternative views of the same dollars; do not add their totals together. When overall variance is near zero, use absolute dollar changes instead of an unstable contribution percentage.

Suggested follow-up questions include:

- Which customers account for the largest settled-spend changes?
- Did spend move between interchange categories?
- Did gross interchange rate or rebate rate change within a category?
- How much of the change comes from refunds?
- Could a missing value or inconsistent synthetic record explain an apparent anomaly?

## Data-quality and rate handling

Check the required fields, complete periods, consistent fictional identities, valid dates, numerical amounts, and the identity `revenue_amount = interchange_amount - rebate_amount`. Use cent-based USD amounts. No real-system joins, source codes, or internal identifiers are needed.

Use the fictional refund categorization and the signed amount convention in the [data requirements](data-contract.md). Keep refunds in the signed totals and explain them separately.

Zero-spend rates are undefined. Negative-spend refund groups remain separate from the ordinary positive-spend rate ranking. A group with negative net revenue and positive spend remains eligible. Flag a small denominator caused by purchase/refund cancellation rather than silently excluding the customer.

## Expected response

Return the question, period scope, dataset reference, metric definitions, headline changes, dollar and rate rankings, relevant anomalies, supporting calculations, follow-up questions, and a human-review status. Tie the explanation to query or function results.

## Planned analysis skills

These responsibilities are planned, not implemented:

1. Validate the synthetic dataset, periods, and metric definitions.
2. Compare spend, interchange, rebates, and net revenue.
3. Investigate interchange mix, rebate rates, and refunds.
4. Rank drivers separately in dollars and basis points.
5. Explain verified results and route them for human review.

Build evaluation cases with known answers before implementing the skills.
