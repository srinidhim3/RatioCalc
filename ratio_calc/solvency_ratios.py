#!/usr/bin/env python3
"""
Solvency Ratios Calculator module.
"""

from typing import Optional, Dict
import pandas as pd


class SolvencyRatios:
    """
    A class for calculating solvency ratios from financial statements and info.
    """

    @staticmethod
    def debt_to_assets_ratio(
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Debt-to-Assets Ratio from the balance sheet for all available periods.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Debt-to-Assets Ratios with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                total_debt = balance_sheet.at["Total Debt", d]
                total_assets = balance_sheet.at["Total Assets", d]

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
                    ratios[d] = None
                else:
                    ratios[d] = debt / assets
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def financial_leverage_ratio(
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Financial Leverage Ratio from the balance sheet for all available periods.

        Args:
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Financial Leverage Ratios with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if balance_sheet is None:
            raise ValueError("Balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                total_assets = balance_sheet.at["Total Assets", d]
                total_equity = balance_sheet.at[
                    "Total Equity Gross Minority Interest", d
                ]

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
                    ratios[d] = None
                else:
                    ratios[d] = assets / equity
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def interest_coverage_ratio(
        income_statement: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Interest Coverage Ratio from the income statement for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.

        Returns:
            dict: The Interest Coverage Ratios with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None:
            raise ValueError("Income statement data is None.")

        ratios = {}
        for d in income_statement.columns:
            try:
                ebit = income_statement.at["EBIT", d]
                interest_expense = income_statement.at["Interest Expense", d]

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
                    ratios[d] = None
                else:
                    ratios[d] = ebit_val / interest
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

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
