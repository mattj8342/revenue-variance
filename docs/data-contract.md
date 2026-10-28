# Synthetic data requirements

## Dataset scope

Each row represents one fictional settled transaction. The demo uses USD and at least two complete monthly periods, with customers and categories represented consistently. Reporting months are derived from settlement date.

Customer names, IDs, vendor names, business lines, categories, and financial values are invented for this project. The dataset is designed independently of real customer records or internal systems.

## Columns

| Column | Dataset field | Definition |
| --- | --- | --- |
| Business line | `business_line` | Business line associated with the transaction. |
| Customer name | `customer_name` | Fictional customer name. |
| Customer ID | `customer_id` | Fictional customer identifier, kept consistent across periods. |
| Vendor name | `vendor_name` | Standardized merchant/vendor name. |
| Settled spend | `spend_amount` | USD amount of the settled transaction. |
| Interchange | `interchange_amount` | Gross interchange dollars before customer rebate. |
| Rebate | `rebate_amount` | Customer rebate dollars paid to the customer. |
| Revenue | `revenue_amount` | Net revenue: interchange minus rebate. This is not profit. |
| Transaction description | `transaction_description` | Interchange categorization, including a distinct refund category. |
| Client segment | `client_segment` | Client segment within the business line. |
| Settlement date | `settlement_date` | Date the transaction settled. |
| Card product | `card_product` | Card product, such as plastic or virtual card. |
| MCC | `mcc` | Merchant category code describing the merchant's business category. |

These are the 13 dataset columns. Customer IDs and MCCs are text values so leading zeros are preserved. Keep each fictional customer's ID and name consistent across periods. Use the same standardized vendor name consistently.

## Financial measures

Store USD amounts to two decimal places. Calculate each transaction's net revenue from the same interchange and rebate amounts so the synthetic records reconcile in cents.

```text
revenue_amount = interchange_amount - rebate_amount
net_revenue_yield = SUM(revenue_amount) / SUM(spend_amount)
gross_interchange_rate = SUM(interchange_amount) / SUM(spend_amount)
rebate_rate = SUM(rebate_amount) / SUM(spend_amount)
rate_change_bps = 10000 * (current_rate - prior_rate)
```

For the same population and spend denominator, net revenue yield equals gross interchange rate minus rebate rate. Calculate rates from amount totals rather than averaging transaction rates. Round rates for display after calculating them.

## Refund scenarios

Use an invented, distinct interchange categorization such as `Refund` to distinguish refunds from regular positive transactions. Define the fictional category labels when generating the dataset.

For the initial synthetic examples, use signed negative spend, interchange, and rebate amounts for a refund that reverses a positive transaction. Compute its net revenue with the same interchange-minus-rebate formula. Keep refunds in the signed totals and show their effect separately in the explanation.

These are fictional demo conventions. No real transaction codes or source-system rules are required.

## Dollar and rate rankings

Rank customers, vendors, and interchange categories separately by net revenue dollar change and by net revenue yield change in basis points.

Include every group with valid positive spend in both periods in the ordinary rate ranking. There is **no minimum-dollar cutoff by default**. Show both periods' spend and the dollar change beside the rate movement.

Zero-spend rates are undefined. Show refund groups with negative spend separately from the ordinary positive-spend ranking. Keep every group's signed financial amounts in the appropriate dollar totals. Negative net revenue with positive spend remains eligible for the rate ranking.

## Evaluation scenarios

| Scenario | Expected finding |
| --- | --- |
| Spend falls while category mix and yield stay steady | Revenue movement is explained by the spend-volume change. |
| Total spend is steady but shifts toward lower-yield categories | Blended yield changes with the category mix. |
| Spend and category shares are steady but within-category yield changes | Identify the within-category rate movement. |
| Spend, interchange, and mix are steady but rebate increases | Net revenue and net revenue yield fall because the rebate rate increased. |
| One large customer drives most of the revenue-dollar change | Highlight that customer in the dollar ranking. |
| A small customer has a large basis-point change | Include it in the valid-rate ranking and show spend and dollar impact alongside it. |
| A refund appears under its distinct categorization | Preserve its signed amounts and explain its effect on totals. |
| A complete demo period is deliberately made incomplete | Flag the coverage anomaly before explaining it as changed customer behavior. |
| A required value is missing | Flag the affected comparison rather than silently replacing the value with zero. |
| The spend denominator is zero | Show dollar amounts and mark the rate undefined. |
| Revenue does not equal interchange minus rebate | Flag the inconsistent synthetic record. |

Record the known expected answers alongside the generated dataset so the analytical calculations and agent explanations can be checked.
