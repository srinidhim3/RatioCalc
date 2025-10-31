The **Defensive Interval Ratio (DIR)** measures the number of days a company can continue to pay its operating expenses with its most liquid assets, without needing to realize its non-current assets or long-term investments.

The formula for the Defensive Interval Ratio is:

$$\text{Defensive Interval Ratio} = \frac{\text{Defensive Assets}}{\text{Daily Operational Expenses}}$$

---

## Defensive Assets

**Defensive Assets** are the most liquid current assets that can be converted to cash quickly. They are typically calculated as:

$$\text{Defensive Assets} = \text{Cash and Cash Equivalents} + \text{Short-Term Marketable Securities} + \text{Net Receivables}$$

Based on the fields available in the **`ITC.NS_balance_sheet.csv`** file, you can approximate Defensive Assets using:

* **Cash And Cash Equivalents**
* **Net Receivables** (The file contains **Receivables** which can be used as a proxy for Net Receivables).

$$\text{Defensive Assets} \approx \text{Cash And Cash Equivalents} + \text{Receivables}$$

---

## Daily Operational Expenses

**Daily Operational Expenses** is the non-cash-related, recurring cost of running the business for one day. It is calculated as:

$$\text{Daily Operational Expenses} = \frac{\text{Annual Operational Expenses}}{\text{Number of Days in the Period (usually 365)}}$$

**Annual Operational Expenses** are typically calculated as:

$$\text{Annual Operational Expenses} = \text{Cost of Goods Sold} + \text{Selling, General, and Administrative Expenses} + \text{Research and Development Expenses} - \text{Non-Cash Charges (like Depreciation and Amortization)}$$

Based on the fields in the **`ITC.NS_income_statement.csv`** file, you can calculate Annual Operational Expenses as:

$$\text{Annual Operational Expenses} \approx \text{Operating Expense} - \text{Depreciation And Amortization}$$

This approximation uses **Operating Expense** as a proxy for the sum of COGS, SG\&A, and R\&D.

---

## Summary of Calculation

In a concise manner, using your data, the Defensive Interval Ratio (in days) can be calculated as:

$$\text{Defensive Interval Ratio} = \frac{\text{Cash And Cash Equivalents} + \text{Receivables}}{\frac{\text{Operating Expense} - \text{Depreciation And Amortization}}{365}}$$

You would need to use the figures for **Cash And Cash Equivalents** and **Receivables** from the **`ITC.NS_balance_sheet.csv`** file, and **Operating Expense** and **Depreciation And Amortization** from the **`ITC.NS_income_statement.csv`** file for the same period.

I'm ready to proceed with the calculation if you specify the year you'd like to analyze.