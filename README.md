# RatioCalc

A Python-based financial ratios calculator that fetches stock data from Yahoo Finance and computes key financial ratios for analysis.

## Features

- Fetch historical stock data and fundamentals (balance sheet, income statement, cash flow) from Yahoo Finance
- Calculate liquidity ratios: Current Ratio, Quick Ratio, Cash Ratio, Defensive Interval Ratio
- Calculate solvency ratios: Debt-to-Equity Ratio, Debt-to-Assets Ratio, Financial Leverage Ratio, Interest Coverage Ratio
- Calculate profitability ratios: Return on Assets (ROA), Return on Equity (ROE)
- Save fetched data to CSV and JSON files for further analysis
- Command-line interface for easy usage

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/srinidhim3/RatioCalc.git
   cd RatioCalc
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script with a stock ticker symbol:

```bash
python main.py
```

The script is currently configured to analyze ITC.NS (ITC Limited on NSE) for the year 2023. You can modify the `ticker`, `start_date`, and `end_date` variables in `main.py` to analyze different stocks or time periods.

Example output includes:
- Historical data preview
- Fundamental data summaries
- Calculated financial ratios

Data files will be saved in the project directory:
- `{ticker}_info.json`
- `{ticker}_balance_sheet.csv`
- `{ticker}_income_statement.csv`
- `{ticker}_cash_flow.csv`

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Project Structure

- `main.py`: Main script for running the analysis
- `yahoo_finance_fetcher.py`: Module for fetching data from Yahoo Finance
- `financial_ratios.py`: Module for calculating financial ratios (placeholder)
- `liquidity_ratios.py`: Module for calculating liquidity ratios
- `solvency_ratios.py`: Module for calculating solvency ratios
- `profitability_ratios.py`: Module for calculating profitability ratios
- `docs/`: Documentation for specific ratios
- `assets/`: Sample data files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
              
This project is open source. Please check the repository for license details.