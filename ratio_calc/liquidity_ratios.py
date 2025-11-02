#!/usr/bin/env python3
"""
Liquidity Ratios Calculator module.
"""

from typing import Optional, Dict
import pandas as pd


class LiquidityRatios:
    """
    A class for calculating liquidity ratios from financial statements.
    """

    @staticmethod
    def current_ratio(
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Current Ratio from the balance sheet for all available periods.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Current Ratios with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                current_assets_val = balance_sheet.at["Current Assets", d]
                current_liabilities_val = balance_sheet.at["Current Liabilities", d]

                def to_float(val, name: str) -> float:
                    if pd.isna(val):
                        raise ValueError(f"{name} is NaN or missing")
                    if isinstance(val, complex):
                        raise TypeError(
                            f"{name} is a complex number and cannot be converted to float"
                        )
                    return float(val)

                current_assets = to_float(current_assets_val, "Current Assets")
                current_liabilities = to_float(
                    current_liabilities_val, "Current Liabilities"
                )

                if current_liabilities == 0:
                    ratios[d] = None  # or raise, but for all_periods, set to None
                else:
                    ratios[d] = current_assets / current_liabilities
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def quick_ratio(
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Quick Ratio (Acid-Test Ratio) from the balance sheet for all available periods.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Quick Ratios with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                cash_equivalents = balance_sheet.at[
                    "Cash Cash Equivalents And Short Term Investments", d
                ]
                accounts_receivable = balance_sheet.at["Accounts Receivable", d]
                current_liabilities = balance_sheet.at["Current Liabilities", d]

                def to_float(val, name: str) -> float:
                    if pd.isna(val):
                        raise ValueError(f"{name} is NaN or missing")
                    if isinstance(val, complex):
                        raise TypeError(
                            f"{name} is a complex number and cannot be converted to float"
                        )
                    return float(val)

                cash_equiv = to_float(
                    cash_equivalents,
                    "Cash Cash Equivalents And Short Term Investments",
                )
                receivables = to_float(accounts_receivable, "Accounts Receivable")
                liabilities = to_float(current_liabilities, "Current Liabilities")

                if liabilities == 0:
                    ratios[d] = None
                else:
                    quick_assets = cash_equiv + receivables
                    ratios[d] = quick_assets / liabilities
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def cash_ratio(
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Cash Ratio from the balance sheet for all available periods.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Cash Ratios with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                cash_equivalents = balance_sheet.at[
                    "Cash Cash Equivalents And Short Term Investments", d
                ]
                current_liabilities = balance_sheet.at["Current Liabilities", d]

                def to_float(val, name: str) -> float:
                    if pd.isna(val):
                        raise ValueError(f"{name} is NaN or missing")
                    if isinstance(val, complex):
                        raise TypeError(
                            f"{name} is a complex number and cannot be converted to float"
                        )
                    return float(val)

                cash_equiv = to_float(
                    cash_equivalents,
                    "Cash Cash Equivalents And Short Term Investments",
                )
                liabilities = to_float(current_liabilities, "Current Liabilities")

                if liabilities == 0:
                    ratios[d] = None
                else:
                    ratios[d] = cash_equiv / liabilities
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def defensive_interval_ratio(
        balance_sheet: pd.DataFrame,
        income_statement: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Defensive Interval Ratio from the balance sheet and income statement for all available periods.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            income_statement (pd.DataFrame): The income statement DataFrame.

        Returns:
            dict: The Defensive Interval Ratios (in days) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if balance_sheet is None or income_statement is None:
            raise ValueError("Balance sheet or income statement data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                cash_equiv = balance_sheet.at["Cash And Cash Equivalents", d]
                receivables = balance_sheet.at["Accounts Receivable", d]
                operating_expense = income_statement.at["Operating Expense", d]
                depreciation = income_statement.at[
                    "Depreciation And Amortization In Income Statement", d
                ]

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
                    depreciation,
                    "Depreciation And Amortization In Income Statement",
                )

                defensive_assets = cash + rec
                annual_op_expenses = op_exp - dep
                daily_op_expenses = annual_op_expenses / 365

                if daily_op_expenses == 0:
                    ratios[d] = None
                else:
                    ratios[d] = defensive_assets / daily_op_expenses
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios
