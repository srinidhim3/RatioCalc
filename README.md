# RatioCalc

A Python-based financial ratios calculator that fetches stock data from Yahoo Finance and computes key financial ratios for analysis.

## Features

- Fetch historical stock data and fundamentals (balance sheet, income statement, cash flow) from Yahoo Finance
- Calculate comprehensive CFA Level 1 financial ratios:
  - **Liquidity Ratios**: Current Ratio, Quick Ratio, Cash Ratio, Defensive Interval Ratio
  - **Solvency Ratios**: Debt-to-Assets Ratio, Financial Leverage Ratio, Interest Coverage Ratio
  - **Profitability Ratios**: Return on Assets (ROA), Return on Equity (ROE), Return on Total Capital, Return on Common Equity
  - **Activity Ratios**: Inventory Turnover, Days of Inventory on Hand, Receivables Turnover, Days of Sales Outstanding, Payables Turnover, Number of Days of Payables, Working Capital Turnover, Fixed Asset Turnover, Total Asset Turnover
  - **DuPont Analysis**: Breakdown of ROE into Net Profit Margin × Asset Turnover × Financial Leverage
- Multi-period analysis with trend tracking across fiscal years
- Clean DataFrame output for programmatic analysis and visualization
- Configurable data cleaning (drop problematic periods)
- Save fetched data to CSV and JSON files for further analysis
- Both command-line and programmatic interfaces

## Installation

### From PyPI (Recommended)
```bash
pip install ratio-calc
```

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/srinidhim3/RatioCalc.git
   cd RatioCalc
   ```

2. Install the package:
   ```bash
   pip install .
   ```

   Or for development:
   ```bash
   pip install -e .
   ```

## Usage

### Command Line Usage

After installation, use the command-line interface:

```bash
ratio-calc ITC.NS
```

Or with options:
```bash
ratio-calc AAPL --start-date 2023-01-01 --end-date 2023-12-31 --drop-periods 2021-03-31
```

### Programmatic Usage

Import and use the `FinancialRatioCalculator` class:

```python
from ratio_calc import FinancialRatioCalculator

# Initialize calculator
calculator = FinancialRatioCalculator(
    ticker="ITC.NS",
    start_date="2023-01-01",
    end_date="2023-12-31",
    drop_periods=["2021-03-31"]  # Optional: drop problematic periods
)

# Run analysis and get DataFrame
df_ratios = calculator.run(verbose=True)

# Access specific ratios
current_ratio_trend = df_ratios.loc['Current Ratio']
roe_comparison = df_ratios.loc[['Return on Equity (ROE)', 'DuPont ROE']]

# Find ratios with highest variation
ratio_variation = df_ratios.std(axis=1).sort_values(ascending=False)
print(f"Most volatile ratios: {ratio_variation.head()}")
```

### Advanced Usage Examples

See `example_usage.py` for comprehensive examples including:
- Basic usage patterns
- Programmatic data analysis
- Custom ratio comparisons
- Statistical analysis of ratio trends

```bash
python example_usage.py
```

## Output

The calculator returns a pandas DataFrame with:
- **Rows**: Ratio names (24+ financial ratios)
- **Columns**: Fiscal periods (e.g., '2025-03-31', '2024-03-31', etc.)

Example DataFrame structure:
```
                                2025-03-31  2024-03-31  2023-03-31  2022-03-31
Current Ratio                     3.062156    2.999587    2.887379    2.814310
Quick Ratio                       1.726978    1.747135    1.807195    1.574858
Return on Equity (ROE)            0.280273    0.265700    0.275985    0.242633
DuPont ROE                        0.280273    0.265700    0.275985    0.242633
...
```

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Project Structure

```
ratio_calc/
├── __init__.py                 # Package initialization and exports
├── calculator.py               # FinancialRatioCalculator class - main entry point
├── yahoo_finance_fetcher.py    # Yahoo Finance data fetching
├── liquidity_ratios.py         # Liquidity ratio calculations
├── solvency_ratios.py          # Solvency ratio calculations
├── profitability_ratios.py     # Profitability ratios and DuPont Analysis
├── activity_ratios.py          # Activity (efficiency) ratio calculations
└── market_ratios.py           # Market ratio calculations (future use)

example_usage.py                # Comprehensive usage examples
docs/                          # Documentation for specific ratios
assets/                        # Sample data files
```

## API Reference

### FinancialRatioCalculator Class

#### Constructor
```python
from ratio_calc import FinancialRatioCalculator

FinancialRatioCalculator(
    ticker: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    drop_periods: Optional[List[str]] = None
)
```

#### Methods
- `fetch_data()`: Fetch fundamental data from Yahoo Finance
- `calculate_ratios()`: Calculate all ratios and return DataFrame
- `run(verbose=True)`: Complete analysis pipeline

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source. Please check the repository for license details.