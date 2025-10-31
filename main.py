#!/usr/bin/env python3
"""
Main script for data science project.
"""

import pprint
import json
from yahoo_finance_fetcher import YahooFinanceFetcher
from liquidity_ratios import LiquidityRatios
from solvency_ratios import SolvencyRatios


if __name__ == "__main__":
    # Example usage
    fetcher = YahooFinanceFetcher()
    ticker = "ITC.NS"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    historical_data = fetcher.fetch_historical_data(ticker, start_date, end_date)
    if historical_data is not None:
        print(f"Historical data for {ticker}:\n", historical_data.head())

    fundamentals = fetcher.fetch_fundamentals(ticker)
    if fundamentals is not None:
        print(f"\nFundamental data for {ticker}:")
        print("Info (Summary):")
        pprint.pprint(fundamentals["info"])
        print("\nBalance Sheet (first 5 rows):")
        print(fundamentals["balance_sheet"].head())
        print("\nIncome Statement (first 5 rows):")
        print(fundamentals["income_statement"].head())
        print("\nCash Flow (first 5 rows):")
        print(fundamentals["cash_flow"].head())

        # Save fundamental data to files
        with open(f"{ticker}_info.json", "w") as f:
            json.dump(fundamentals["info"], f, indent=4)
        fundamentals["balance_sheet"].to_csv(f"{ticker}_balance_sheet.csv")
        fundamentals["income_statement"].to_csv(f"{ticker}_income_statement.csv")
        fundamentals["cash_flow"].to_csv(f"{ticker}_cash_flow.csv")
        print(
            f"\nFundamental data saved to {ticker}_info.json, {ticker}_balance_sheet.csv, {ticker}_income_statement.csv, and {ticker}_cash_flow.csv"
        )

        # Calculate ratios
        latest_date = fundamentals["balance_sheet"].columns[0]
        # Calculate Current Ratio (liquidity ratios)
        try:
            current_ratio = LiquidityRatios.current_ratio(fundamentals["balance_sheet"])
            print(
                f"\nCalculated Current Ratio for {ticker} ({latest_date}): {current_ratio:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Current Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Current Ratio: {e}")

        # Calculate Quick Ratio
        try:
            quick_ratio = LiquidityRatios.quick_ratio(fundamentals["balance_sheet"])
            print(
                f"Calculated Quick Ratio for {ticker} ({latest_date}): {quick_ratio:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Quick Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Quick Ratio: {e}")

        # Calculate Cash Ratio
        try:
            cash_ratio = LiquidityRatios.cash_ratio(fundamentals["balance_sheet"])
            print(
                f"Calculated Cash Ratio for {ticker} ({latest_date}): {cash_ratio:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Cash Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Cash Ratio: {e}")

        # Calculate Debt-to-Assets Ratio (next ratio to be calculated)
        try:
            debt_to_assets = SolvencyRatios.debt_to_assets_ratio(
                fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Debt-to-Assets Ratio for {ticker} ({latest_date}): {debt_to_assets:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Debt-to-Assets Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Debt-to-Assets Ratio: {e}")

        # Calculate Debt-to-Equity Ratio from info
        try:
            debt_to_equity = SolvencyRatios.debt_to_equity_ratio_from_info(
                fundamentals["info"]
            )
            print(
                f"Debt-to-Equity Ratio for {ticker} (from Yahoo Finance): {debt_to_equity:.6f}"
            )
        except KeyError as e:
            print(f"Error retrieving Debt-to-Equity Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Debt-to-Equity Ratio: {e}")

        # Calculate Financial Leverage Ratio
        try:
            financial_leverage = SolvencyRatios.financial_leverage_ratio(
                fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Financial Leverage Ratio for {ticker} ({latest_date}): {financial_leverage:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Financial Leverage Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Financial Leverage Ratio: {e}")

        # Calculate Interest Coverage Ratio
        try:
            interest_coverage = SolvencyRatios.interest_coverage_ratio(
                fundamentals["income_statement"]
            )
            print(
                f"Calculated Interest Coverage Ratio for {ticker} ({latest_date}): {interest_coverage:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Interest Coverage Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Interest Coverage Ratio: {e}")

        # Calculate Defensive Interval Ratio
        try:
            dir_ratio = LiquidityRatios.defensive_interval_ratio(
                fundamentals["balance_sheet"], fundamentals["income_statement"]
            )
            print(
                f"Calculated Defensive Interval Ratio for {ticker} ({latest_date}): {dir_ratio:.6f} days"
            )
        except KeyError as e:
            print(f"Error calculating Defensive Interval Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Defensive Interval Ratio: {e}")
