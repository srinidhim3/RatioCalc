#!/usr/bin/env python3
"""
Solvency Ratios Calculator module.
"""

from typing import Optional
import pandas as pd


class SolvencyRatios:
    """
    A class for calculating solvency ratios from financial statements and info.
    """

    @staticmethod
    def debt_to_assets_ratio(
        balance_sheet: pd.DataFrame, date: Optional[str] = None
    ) -> float:
        """
        Calculates the Debt-to-Assets Ratio from the balance sheet.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Debt-to-Assets Ratio.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If total assets are zero.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            total_debt = balance_sheet.at["Total Debt", date]
            total_assets = balance_sheet.at["Total Assets", date]
        except KeyError as e:
            raise KeyError(f"Required key missing in balance sheet: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        debt = to_float(total_debt, "Total Debt")
        assets = to_float(total_assets, "Total Assets")

        if assets == 0:
            raise ZeroDivisionError("Total assets are zero.")
        return debt / assets

    @staticmethod
    def financial_leverage_ratio(
        balance_sheet: pd.DataFrame, date: Optional[str] = None
    ) -> float:
        """
        Calculates the Financial Leverage Ratio from the balance sheet.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Financial Leverage Ratio.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If total equity is zero.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            total_assets = balance_sheet.at["Total Assets", date]
            total_equity = balance_sheet.at[
                "Total Equity Gross Minority Interest", date
            ]
        except KeyError as e:
            raise KeyError(f"Required key missing in balance sheet: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        assets = to_float(total_assets, "Total Assets")
        equity = to_float(total_equity, "Total Equity Gross Minority Interest")

        if equity == 0:
            raise ZeroDivisionError("Total equity is zero.")
        return assets / equity

    @staticmethod
    def interest_coverage_ratio(
        income_statement: pd.DataFrame, date: Optional[str] = None
    ) -> float:
        """
        Calculates the Interest Coverage Ratio from the income statement.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Interest Coverage Ratio.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If interest expense is zero.
        """
        if income_statement is None:
            raise ValueError("Income statement data is None.")

        if date is None:
            date = income_statement.columns[0]  # Latest date

        try:
            ebit = income_statement.at["EBIT", date]
            interest_expense = income_statement.at["Interest Expense", date]
        except KeyError as e:
            raise KeyError(f"Required key missing in income statement: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        ebit_val = to_float(ebit, "EBIT")
        interest = to_float(interest_expense, "Interest Expense")

        if interest == 0:
            raise ZeroDivisionError("Interest expense is zero.")
        return ebit_val / interest

    @staticmethod
    def debt_to_equity_ratio_from_info(info: dict) -> float:
        """
        Retrieves the Debt-to-Equity Ratio from the Yahoo Finance info data.

        Args:
            info (dict): The info dictionary from Yahoo Finance.

        Returns:
            float: The Debt-to-Equity Ratio.

        Raises:
            KeyError: If 'debtToEquity' key is missing.
            ValueError: If the value is NaN or invalid.
        """
        if info is None:
            raise ValueError("Info data is None.")

        try:
            debt_to_equity = info["debtToEquity"]
        except KeyError:
            raise KeyError("Required key 'debtToEquity' missing in info")

        if pd.isna(debt_to_equity):
            raise ValueError("Debt-to-Equity Ratio is NaN or missing")

        return float(debt_to_equity)
