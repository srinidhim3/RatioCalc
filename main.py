#!/usr/bin/env python3
"""
Financial Ratio Calculator - Main entry point class for calculating comprehensive financial ratios.

This module provides the FinancialRatioCalculator class, which serves as the primary interface
for fetching Yahoo Finance data and calculating financial ratios across multiple periods.

Key Features:
- Fetches balance sheet, income statement, and cash flow data from Yahoo Finance
- Calculates 24+ financial ratios including liquidity, solvency, profitability, activity, and DuPont analysis
- Returns clean pandas DataFrame for programmatic analysis
- Supports data cleaning (dropping problematic periods)
- Saves raw data and results to CSV files

Basic Usage:
    from main import FinancialRatioCalculator

    calculator = FinancialRatioCalculator(ticker="ITC.NS", drop_periods=["2021-03-31"])
    df_ratios = calculator.run()

    # Access specific ratios
    current_ratio = df_ratios.loc['Current Ratio']
    roe_trend = df_ratios.loc['Return on Equity (ROE)']

Command Line Usage:
    python main.py

For comprehensive examples, see example_usage.py
"""

import json
from typing import Dict, List, Optional, Any
import pandas as pd
from yahoo_finance_fetcher import YahooFinanceFetcher
from liquidity_ratios import LiquidityRatios
from solvency_ratios import SolvencyRatios
from profitability_ratios import ProfitabilityRatios
from activity_ratios import ActivityRatios


class FinancialRatioCalculator:
    """
    A class for calculating comprehensive financial ratios from Yahoo Finance data.

    This class provides methods to fetch financial data and calculate all major
    categories of financial ratios including liquidity, solvency, profitability,
    activity, and DuPont analysis components.
    """

    def __init__(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        drop_periods: Optional[List[str]] = None,
    ):
        """
        Initialize the Financial Ratio Calculator.

        Args:
            ticker (str): Stock ticker symbol (e.g., 'ITC.NS')
            start_date (str, optional): Start date for historical data in YYYY-MM-DD format
            end_date (str, optional): End date for historical data in YYYY-MM-DD format
            drop_periods (list, optional): List of period columns to drop (e.g., ['2021-03-31'])
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.drop_periods = drop_periods or []
        self.fetcher = YahooFinanceFetcher()
        self.fundamentals: Optional[Dict[str, Any]] = None
        self.historical_data: Optional[pd.DataFrame] = None

    def fetch_data(self, save_files=True):
        """
        Fetch historical and fundamental data from Yahoo Finance.

        Args:
            save_files (bool): Whether to save raw data to CSV/JSON files

        Returns:
            dict: Dictionary containing 'fundamentals' and 'historical_data'

        Raises:
            Exception: If data fetching fails
        """
        # Fetch historical data
        if self.start_date and self.end_date:
            self.historical_data = self.fetcher.fetch_historical_data(
                self.ticker, self.start_date, self.end_date
            )

        # Fetch fundamental data
        self.fundamentals = self.fetcher.fetch_fundamentals(self.ticker)
        if self.fundamentals is None:
            raise Exception(f"Failed to fetch fundamental data for {self.ticker}")

        # Save raw data if requested
        if save_files:
            self._save_raw_data()

        # Clean data by dropping specified periods
        self._clean_data()

        return {
            "fundamentals": self.fundamentals,
            "historical_data": self.historical_data,
        }

    def _save_raw_data(self) -> None:
        """Save raw fundamental data to files."""
        assert self.fundamentals is not None  # Already checked in fetch_data

        with open(f"{self.ticker}_info.json", "w") as f:
            json.dump(self.fundamentals["info"], f, indent=4)
        self.fundamentals["balance_sheet"].to_csv(f"{self.ticker}_balance_sheet.csv")
        self.fundamentals["income_statement"].to_csv(
            f"{self.ticker}_income_statement.csv"
        )
        self.fundamentals["cash_flow"].to_csv(f"{self.ticker}_cash_flow.csv")
        print(
            f"\nFundamental data saved to {self.ticker}_info.json, {self.ticker}_balance_sheet.csv, "
            f"{self.ticker}_income_statement.csv, and {self.ticker}_cash_flow.csv"
        )

    def _clean_data(self) -> None:
        """Clean the data by dropping specified periods."""
        assert self.fundamentals is not None  # Already checked in fetch_data

        if self.drop_periods:
            for df_name in ["balance_sheet", "income_statement", "cash_flow"]:
                if df_name in self.fundamentals:
                    self.fundamentals[df_name] = self.fundamentals[df_name].drop(
                        columns=self.drop_periods, errors="ignore"
                    )

    def calculate_ratios(self) -> pd.DataFrame:
        """
        Calculate all financial ratios and return as a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing all calculated ratios with dates as columns

        Raises:
            Exception: If fundamentals data is not available
        """
        if self.fundamentals is None:
            raise Exception("Fundamentals data not available. Call fetch_data() first.")

        ratios_multi: Dict[str, Dict[str, Optional[float]]] = {}

        # Calculate Liquidity Ratios
        self._calculate_liquidity_ratios(ratios_multi)

        # Calculate Solvency Ratios
        self._calculate_solvency_ratios(ratios_multi)

        # Calculate Profitability Ratios
        self._calculate_profitability_ratios(ratios_multi)

        # Calculate Activity Ratios
        self._calculate_activity_ratios(ratios_multi)

        # Calculate DuPont Analysis components
        self._calculate_dupont_analysis(ratios_multi)

        # Create and return DataFrame
        if ratios_multi:
            df = pd.DataFrame(ratios_multi)
            return df.T  # Transpose so ratios are index, dates are columns
        else:
            return pd.DataFrame()

    def _calculate_liquidity_ratios(
        self, ratios_dict: Dict[str, Dict[str, Optional[float]]]
    ) -> None:
        """Calculate liquidity ratios."""
        assert self.fundamentals is not None  # Already checked in calculate_ratios

        try:
            current_ratio = LiquidityRatios.current_ratio(
                self.fundamentals["balance_sheet"]
            )
            ratios_dict["Current Ratio"] = current_ratio
        except Exception as e:
            print(f"Error calculating Current Ratio: {e}")

        try:
            quick_ratio = LiquidityRatios.quick_ratio(
                self.fundamentals["balance_sheet"]
            )
            ratios_dict["Quick Ratio"] = quick_ratio
        except Exception as e:
            print(f"Error calculating Quick Ratio: {e}")

        try:
            cash_ratio = LiquidityRatios.cash_ratio(self.fundamentals["balance_sheet"])
            ratios_dict["Cash Ratio"] = cash_ratio
        except Exception as e:
            print(f"Error calculating Cash Ratio: {e}")

        try:
            dir_ratio = LiquidityRatios.defensive_interval_ratio(
                self.fundamentals["balance_sheet"],
                self.fundamentals["income_statement"],
            )
            ratios_dict["Defensive Interval Ratio"] = dir_ratio
        except Exception as e:
            print(f"Error calculating Defensive Interval Ratio: {e}")

    def _calculate_solvency_ratios(
        self, ratios_dict: Dict[str, Dict[str, Optional[float]]]
    ) -> None:
        """Calculate solvency ratios."""
        assert self.fundamentals is not None  # Already checked in calculate_ratios

        try:
            debt_to_assets = SolvencyRatios.debt_to_assets_ratio(
                self.fundamentals["balance_sheet"]
            )
            ratios_dict["Debt-to-Assets Ratio"] = debt_to_assets
        except Exception as e:
            print(f"Error calculating Debt-to-Assets Ratio: {e}")

        try:
            financial_leverage = SolvencyRatios.financial_leverage_ratio(
                self.fundamentals["balance_sheet"]
            )
            ratios_dict["Financial Leverage Ratio"] = financial_leverage
        except Exception as e:
            print(f"Error calculating Financial Leverage Ratio: {e}")

        try:
            interest_coverage = SolvencyRatios.interest_coverage_ratio(
                self.fundamentals["income_statement"]
            )
            ratios_dict["Interest Coverage Ratio"] = interest_coverage
        except Exception as e:
            print(f"Error calculating Interest Coverage Ratio: {e}")

    def _calculate_profitability_ratios(
        self, ratios_dict: Dict[str, Dict[str, Optional[float]]]
    ) -> None:
        """Calculate profitability ratios."""
        assert self.fundamentals is not None  # Already checked in calculate_ratios

        try:
            roa = ProfitabilityRatios.return_on_assets(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Return on Assets (ROA)"] = roa
        except Exception as e:
            print(f"Error calculating Return on Assets (ROA): {e}")

        try:
            roe = ProfitabilityRatios.return_on_equity(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Return on Equity (ROE)"] = roe
        except Exception as e:
            print(f"Error calculating Return on Equity (ROE): {e}")

        try:
            rotc = ProfitabilityRatios.return_on_total_capital(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Return on Total Capital (ROTC)"] = rotc
        except Exception as e:
            print(f"Error calculating Return on Total Capital (ROTC): {e}")

        try:
            roce = ProfitabilityRatios.return_on_common_equity(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Return on Common Equity (ROCE)"] = roce
        except Exception as e:
            print(f"Error calculating Return on Common Equity (ROCE): {e}")

    def _calculate_activity_ratios(
        self, ratios_dict: Dict[str, Dict[str, Optional[float]]]
    ) -> None:
        """Calculate activity ratios."""
        assert self.fundamentals is not None  # Already checked in calculate_ratios

        try:
            inventory_turnover = ActivityRatios.inventory_turnover(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Inventory Turnover"] = inventory_turnover
        except Exception as e:
            print(f"Error calculating Inventory Turnover: {e}")

        try:
            doh = ActivityRatios.days_of_inventory_on_hand(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Days of Inventory on Hand (DOH)"] = doh
        except Exception as e:
            print(f"Error calculating Days of Inventory on Hand (DOH): {e}")

        try:
            receivables_turnover = ActivityRatios.receivables_turnover(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Receivables Turnover"] = receivables_turnover
        except Exception as e:
            print(f"Error calculating Receivables Turnover: {e}")

        try:
            dso = ActivityRatios.days_of_sales_outstanding(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Days of Sales Outstanding (DSO)"] = dso
        except Exception as e:
            print(f"Error calculating Days of Sales Outstanding (DSO): {e}")

        try:
            payables_turnover = ActivityRatios.payables_turnover(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Payables Turnover"] = payables_turnover
        except Exception as e:
            print(f"Error calculating Payables Turnover: {e}")

        try:
            days_payables = ActivityRatios.number_of_days_of_payables(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Number of Days of Payables"] = days_payables
        except Exception as e:
            print(f"Error calculating Number of Days of Payables: {e}")

        try:
            wc_turnover = ActivityRatios.working_capital_turnover(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Working Capital Turnover"] = wc_turnover
        except Exception as e:
            print(f"Error calculating Working Capital Turnover: {e}")

        try:
            fa_turnover = ActivityRatios.fixed_asset_turnover(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Fixed Asset Turnover"] = fa_turnover
        except Exception as e:
            print(f"Error calculating Fixed Asset Turnover: {e}")

        try:
            ta_turnover = ActivityRatios.total_asset_turnover(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
            )
            ratios_dict["Total Asset Turnover"] = ta_turnover
        except Exception as e:
            print(f"Error calculating Total Asset Turnover: {e}")

    def _calculate_dupont_analysis(
        self, ratios_dict: Dict[str, Dict[str, Optional[float]]]
    ) -> None:
        """Calculate DuPont analysis components."""
        assert self.fundamentals is not None  # Already checked in calculate_ratios

        try:
            dupont = ProfitabilityRatios.dupont_analysis(
                self.fundamentals["income_statement"],
                self.fundamentals["balance_sheet"],
                self.fundamentals["info"],
            )

            # Add DuPont components to ratios_dict
            dupont_roe = {}
            dupont_npm = {}
            dupont_at = {}
            dupont_fl = {}

            for date, components in dupont.items():
                dupont_roe[date] = components.get("roe")
                dupont_npm[date] = components.get("net_profit_margin")
                dupont_at[date] = components.get("asset_turnover")
                dupont_fl[date] = components.get("financial_leverage")

            ratios_dict["DuPont ROE"] = dupont_roe
            ratios_dict["DuPont Net Profit Margin"] = dupont_npm
            ratios_dict["DuPont Asset Turnover"] = dupont_at
            ratios_dict["DuPont Financial Leverage"] = dupont_fl

        except Exception as e:
            print(f"Error calculating DuPont Analysis: {e}")

    def run(self, save_csv: bool = True, verbose: bool = True) -> pd.DataFrame:
        """
        Run the complete analysis: fetch data, calculate ratios, and optionally save results.

        Args:
            save_csv (bool): Whether to save the ratios DataFrame to CSV
            verbose (bool): Whether to print progress information

        Returns:
            pd.DataFrame: DataFrame containing all calculated ratios
        """
        if verbose:
            print(f"Fetching data for {self.ticker}...")

        # Fetch data
        self.fetch_data()

        if verbose:
            print("Calculating ratios...")

        # Calculate ratios
        df_ratios = self.calculate_ratios()

        # Save to CSV if requested
        if save_csv and not df_ratios.empty:
            csv_filename = f"{self.ticker}_multi_period_ratios.csv"
            df_ratios.to_csv(csv_filename)
            if verbose:
                print(f"\nMulti-period ratios saved to {csv_filename}")

        if verbose and not df_ratios.empty:
            print(f"\nMulti-period Ratios for {self.ticker}:")
            print(df_ratios.to_string())

        return df_ratios


if __name__ == "__main__":
    # Example usage
    calculator = FinancialRatioCalculator(
        ticker="ITC.NS",
        start_date="2023-01-01",
        end_date="2023-12-31",
        drop_periods=["2021-03-31"],
    )

    # Run the analysis
    df_ratios = calculator.run()

    # Example of programmatic usage:
    # calculator = FinancialRatioCalculator(ticker="AAPL")
    # df = calculator.run(save_csv=False, verbose=False)
    # print(f"AAPL has {len(df.columns)} periods of data")
    # print(f"Current Ratio trend: {df.loc['Current Ratio'].tolist()}")
