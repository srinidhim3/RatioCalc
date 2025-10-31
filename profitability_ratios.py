#!/usr/bin/env python3
"""
Profitability Ratios Calculator module.
"""

from typing import Optional
import pandas as pd


class ProfitabilityRatios:
    """
    A class for calculating profitability ratios from financial statements.
    """

    @staticmethod
    def return_on_assets(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Return on Assets (ROA) from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Return on Assets (ROA).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If total assets are zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            net_income = income_statement.at[
                "Net Income From Continuing Operation Net Minority Interest", date
            ]
            total_assets = balance_sheet.at["Total Assets", date]
        except KeyError as e:
            raise KeyError(f"Required key missing: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        net_inc = to_float(
            net_income, "Net Income From Continuing Operation Net Minority Interest"
        )
        assets = to_float(total_assets, "Total Assets")

        if assets == 0:
            raise ZeroDivisionError("Total assets are zero.")
        return net_inc / assets

    @staticmethod
    def return_on_equity(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Return on Equity (ROE) from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Return on Equity (ROE).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If shareholders' equity is zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            net_income = income_statement.at[
                "Net Income From Continuing Operation Net Minority Interest", date
            ]
            shareholders_equity = balance_sheet.at[
                "Total Equity Gross Minority Interest", date
            ]
        except KeyError as e:
            raise KeyError(f"Required key missing: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        net_inc = to_float(
            net_income, "Net Income From Continuing Operation Net Minority Interest"
        )
        equity = to_float(shareholders_equity, "Total Equity Gross Minority Interest")

        if equity == 0:
            raise ZeroDivisionError("Shareholders' equity is zero.")
        return net_inc / equity

    @staticmethod
    def return_on_total_capital(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Return on Total Capital (ROTC) from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Return on Total Capital (ROTC).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If total capital (debt + equity) is zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            ebit = income_statement.at["EBIT", date]
            total_debt = balance_sheet.at["Total Debt", date]
            total_equity = balance_sheet.at[
                "Total Equity Gross Minority Interest", date
            ]
        except KeyError as e:
            raise KeyError(f"Required key missing: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        ebit_val = to_float(ebit, "EBIT")
        debt = to_float(total_debt, "Total Debt")
        equity = to_float(total_equity, "Total Equity Gross Minority Interest")

        total_capital = debt + equity
        if total_capital == 0:
            raise ZeroDivisionError("Total capital (debt + equity) is zero.")
        return ebit_val / total_capital

    @staticmethod
    def return_on_common_equity(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Return on Common Equity (ROCE) from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Return on Common Equity (ROCE).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If common shareholders' equity is zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            net_income = income_statement.at[
                "Net Income From Continuing Operation Net Minority Interest", date
            ]
            common_equity = balance_sheet.at[
                "Total Equity Gross Minority Interest", date
            ]
        except KeyError as e:
            raise KeyError(f"Required key missing: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        net_inc = to_float(
            net_income, "Net Income From Continuing Operation Net Minority Interest"
        )
        equity = to_float(common_equity, "Total Equity Gross Minority Interest")

        if equity == 0:
            raise ZeroDivisionError("Common shareholders' equity is zero.")
        return net_inc / equity
