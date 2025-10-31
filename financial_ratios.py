#!/usr/bin/env python3
"""
Financial Ratios Calculator module.
"""

from typing import Optional
import pandas as pd


class FinancialRatiosCalculator:
    """
    A class for calculating financial ratios from financial statements.
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
        print(f"Debt: {debt}, Assets: {assets}")
        return debt / assets
