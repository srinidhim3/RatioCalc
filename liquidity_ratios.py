#!/usr/bin/env python3
"""
Liquidity Ratios Calculator module.
"""

from typing import Optional
import pandas as pd


class LiquidityRatios:
    """
    A class for calculating liquidity ratios from financial statements.
    """

    @staticmethod
    def current_ratio(balance_sheet: pd.DataFrame, date: Optional[str] = None) -> float:
        """
        Calculates the Current Ratio from the balance sheet.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Current Ratio.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If current liabilities are zero.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            current_assets_val = balance_sheet.at["Current Assets", date]
            current_liabilities_val = balance_sheet.at["Current Liabilities", date]
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

        current_assets = to_float(current_assets_val, "Current Assets")
        current_liabilities = to_float(current_liabilities_val, "Current Liabilities")

        if current_liabilities == 0:
            raise ZeroDivisionError("Current liabilities are zero.")

        return current_assets / current_liabilities

    @staticmethod
    def quick_ratio(balance_sheet: pd.DataFrame, date: Optional[str] = None) -> float:
        """
        Calculates the Quick Ratio (Acid-Test Ratio) from the balance sheet.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Quick Ratio.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If current liabilities are zero.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            cash_equivalents = balance_sheet.at[
                "Cash Cash Equivalents And Short Term Investments", date
            ]
            accounts_receivable = balance_sheet.at["Accounts Receivable", date]
            current_liabilities = balance_sheet.at["Current Liabilities", date]
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

        cash_equiv = to_float(
            cash_equivalents, "Cash Cash Equivalents And Short Term Investments"
        )
        receivables = to_float(accounts_receivable, "Accounts Receivable")
        liabilities = to_float(current_liabilities, "Current Liabilities")

        if liabilities == 0:
            raise ZeroDivisionError("Current liabilities are zero.")

        quick_assets = cash_equiv + receivables
        return quick_assets / liabilities

    @staticmethod
    def cash_ratio(balance_sheet: pd.DataFrame, date: Optional[str] = None) -> float:
        """
        Calculates the Cash Ratio from the balance sheet.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Cash Ratio.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If current liabilities are zero.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            cash_equivalents = balance_sheet.at[
                "Cash Cash Equivalents And Short Term Investments", date
            ]
            current_liabilities = balance_sheet.at["Current Liabilities", date]
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

        cash_equiv = to_float(
            cash_equivalents, "Cash Cash Equivalents And Short Term Investments"
        )
        liabilities = to_float(current_liabilities, "Current Liabilities")

        if liabilities == 0:
            raise ZeroDivisionError("Current liabilities are zero.")

        return cash_equiv / liabilities

    @staticmethod
    def defensive_interval_ratio(
        balance_sheet: pd.DataFrame,
        income_statement: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Defensive Interval Ratio from the balance sheet and income statement.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            income_statement (pd.DataFrame): The income statement DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Defensive Interval Ratio (in days).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If daily operational expenses are zero.
        """
        if balance_sheet is None or income_statement is None:
            raise ValueError("Balance sheet or income statement data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            cash_equiv = balance_sheet.at["Cash And Cash Equivalents", date]
            receivables = balance_sheet.at["Accounts Receivable", date]
            operating_expense = income_statement.at["Operating Expense", date]
            depreciation = income_statement.at[
                "Depreciation And Amortization In Income Statement", date
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

        cash = to_float(cash_equiv, "Cash And Cash Equivalents")
        rec = to_float(receivables, "Accounts Receivable")
        op_exp = to_float(operating_expense, "Operating Expense")
        dep = to_float(
            depreciation, "Depreciation And Amortization In Income Statement"
        )

        defensive_assets = cash + rec
        annual_op_expenses = op_exp - dep
        daily_op_expenses = annual_op_expenses / 365

        if daily_op_expenses == 0:
            raise ZeroDivisionError("Daily operational expenses are zero.")

        return defensive_assets / daily_op_expenses
