#!/usr/bin/env python3
"""
Activity Ratios Calculator module.
"""

from typing import Optional
import pandas as pd


class ActivityRatios:
    """
    A class for calculating activity (efficiency) ratios from financial statements.
    """

    @staticmethod
    def inventory_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Inventory Turnover from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Inventory Turnover.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If average inventory is zero.
            ValueError: If insufficient data for average calculation.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()
        if len(dates) < 2:
            raise ValueError(
                "Insufficient balance sheet data for average inventory calculation."
            )

        if date is None:
            date = dates[0]  # Latest date
            prev_date = dates[1]  # Previous date
        else:
            if date not in dates:
                raise ValueError(f"Date {date} not found in balance sheet.")
            idx = dates.index(date)
            if idx + 1 >= len(dates):
                raise ValueError(
                    "No previous date available for average inventory calculation."
                )
            prev_date = dates[idx + 1]

        try:
            cogs = income_statement.at["Cost Of Revenue", date]
            inventory_end = balance_sheet.at["Inventory", date]
            inventory_begin = balance_sheet.at["Inventory", prev_date]
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

        cogs_val = to_float(cogs, "Cost Of Revenue")
        inv_end = to_float(inventory_end, "Inventory (ending)")
        inv_begin = to_float(inventory_begin, "Inventory (beginning)")

        avg_inventory = (inv_begin + inv_end) / 2
        if avg_inventory == 0:
            raise ZeroDivisionError("Average inventory is zero.")
        return cogs_val / avg_inventory

    @staticmethod
    def days_of_inventory_on_hand(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Days of Inventory on Hand (DOH) from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Days of Inventory on Hand (DOH).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If inventory turnover is zero.
            ValueError: If insufficient data for average calculation.
        """
        turnover = ActivityRatios.inventory_turnover(
            income_statement, balance_sheet, date
        )
        if turnover == 0:
            raise ZeroDivisionError("Inventory turnover is zero.")
        return 365 / turnover

    @staticmethod
    def receivables_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Receivables Turnover from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Receivables Turnover.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If average accounts receivable is zero.
            ValueError: If insufficient data for average calculation.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()
        if len(dates) < 2:
            raise ValueError(
                "Insufficient balance sheet data for average accounts receivable calculation."
            )

        if date is None:
            date = dates[0]  # Latest date
            prev_date = dates[1]  # Previous date
        else:
            if date not in dates:
                raise ValueError(f"Date {date} not found in balance sheet.")
            idx = dates.index(date)
            if idx + 1 >= len(dates):
                raise ValueError(
                    "No previous date available for average accounts receivable calculation."
                )
            prev_date = dates[idx + 1]

        try:
            revenue = income_statement.at["Total Revenue", date]
            receivables_end = balance_sheet.at["Accounts Receivable", date]
            receivables_begin = balance_sheet.at["Accounts Receivable", prev_date]
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

        revenue_val = to_float(revenue, "Total Revenue")
        rec_end = to_float(receivables_end, "Accounts Receivable (ending)")
        rec_begin = to_float(receivables_begin, "Accounts Receivable (beginning)")

        avg_receivables = (rec_begin + rec_end) / 2
        if avg_receivables == 0:
            raise ZeroDivisionError("Average accounts receivable is zero.")
        return revenue_val / avg_receivables

    @staticmethod
    def days_of_sales_outstanding(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Days of Sales Outstanding (DSO) from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Days of Sales Outstanding (DSO).

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If receivables turnover is zero.
            ValueError: If insufficient data for average calculation.
        """
        turnover = ActivityRatios.receivables_turnover(
            income_statement, balance_sheet, date
        )
        if turnover == 0:
            raise ZeroDivisionError("Receivables turnover is zero.")
        return 365 / turnover

    @staticmethod
    def payables_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Payables Turnover from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Payables Turnover.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If average accounts payable is zero.
            ValueError: If insufficient data for average calculation.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()
        if len(dates) < 2:
            raise ValueError(
                "Insufficient balance sheet data for average accounts payable calculation."
            )

        if date is None:
            date = dates[0]  # Latest date
            prev_date = dates[1]  # Previous date
        else:
            if date not in dates:
                raise ValueError(f"Date {date} not found in balance sheet.")
            idx = dates.index(date)
            if idx + 1 >= len(dates):
                raise ValueError(
                    "No previous date available for average accounts payable calculation."
                )
            prev_date = dates[idx + 1]

        try:
            cogs = income_statement.at["Cost Of Revenue", date]
            payables_end = balance_sheet.at["Accounts Payable", date]
            payables_begin = balance_sheet.at["Accounts Payable", prev_date]
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

        cogs_val = to_float(cogs, "Cost Of Revenue")
        pay_end = to_float(payables_end, "Accounts Payable (ending)")
        pay_begin = to_float(payables_begin, "Accounts Payable (beginning)")

        avg_payables = (pay_begin + pay_end) / 2
        if avg_payables == 0:
            raise ZeroDivisionError("Average accounts payable is zero.")
        return cogs_val / avg_payables

    @staticmethod
    def number_of_days_of_payables(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Number of Days of Payables from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Number of Days of Payables.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If payables turnover is zero.
            ValueError: If insufficient data for average calculation.
        """
        turnover = ActivityRatios.payables_turnover(
            income_statement, balance_sheet, date
        )
        if turnover == 0:
            raise ZeroDivisionError("Payables turnover is zero.")
        return 365 / turnover

    @staticmethod
    def working_capital_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Working Capital Turnover from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Working Capital Turnover.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If working capital is zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            revenue = income_statement.at["Total Revenue", date]
            current_assets = balance_sheet.at["Current Assets", date]
            current_liabilities = balance_sheet.at["Current Liabilities", date]
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

        revenue_val = to_float(revenue, "Total Revenue")
        ca = to_float(current_assets, "Current Assets")
        cl = to_float(current_liabilities, "Current Liabilities")

        working_capital = ca - cl
        if working_capital == 0:
            raise ZeroDivisionError("Working capital is zero.")
        return revenue_val / working_capital

    @staticmethod
    def fixed_asset_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Fixed Asset Turnover from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Fixed Asset Turnover.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If net fixed assets is zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            revenue = income_statement.at["Total Revenue", date]
            net_fixed_assets = balance_sheet.at["Net PPE", date]
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

        revenue_val = to_float(revenue, "Total Revenue")
        nfa = to_float(net_fixed_assets, "Net PPE")

        if nfa == 0:
            raise ZeroDivisionError("Net fixed assets is zero.")
        return revenue_val / nfa

    @staticmethod
    def total_asset_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        date: Optional[str] = None,
    ) -> float:
        """
        Calculates the Total Asset Turnover from the income statement and balance sheet.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            date (str, optional): The date column to use (e.g., '2025-03-31'). If None, uses the latest date.

        Returns:
            float: The Total Asset Turnover.

        Raises:
            KeyError: If required keys are missing.
            ZeroDivisionError: If total assets is zero.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        if date is None:
            date = balance_sheet.columns[0]  # Latest date

        try:
            revenue = income_statement.at["Total Revenue", date]
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

        revenue_val = to_float(revenue, "Total Revenue")
        ta = to_float(total_assets, "Total Assets")

        if ta == 0:
            raise ZeroDivisionError("Total assets is zero.")
        return revenue_val / ta
