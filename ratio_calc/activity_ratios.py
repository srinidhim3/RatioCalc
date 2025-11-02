#!/usr/bin/env python3
"""
Activity Ratios Calculator module.
"""

from typing import Dict, Optional
import pandas as pd


class ActivityRatios:
    """
    A class for calculating activity (efficiency) ratios from financial statements.
    """

    @staticmethod
    def inventory_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Inventory Turnover from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Inventory Turnovers with dates as keys.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If insufficient data for average calculation.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()
        if len(dates) < 2:
            raise ValueError(
                "Insufficient balance sheet data for average inventory calculation."
            )

        ratios = {}
        for i in range(len(dates) - 1):
            current_period = dates[i]
            previous_period = dates[i + 1]
            try:
                cogs = income_statement.at["Cost Of Revenue", current_period]
                inventory_end = balance_sheet.at["Inventory", current_period]
                inventory_begin = balance_sheet.at["Inventory", previous_period]

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
                    ratios[current_period] = None
                else:
                    ratios[current_period] = cogs_val / avg_inventory
            except (KeyError, ValueError, TypeError):
                ratios[current_period] = None
        return ratios

    @staticmethod
    def days_of_inventory_on_hand(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Days of Inventory on Hand (DOH) from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Days of Inventory on Hand (DOH) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If insufficient data for average calculation.
        """
        turnover = ActivityRatios.inventory_turnover(income_statement, balance_sheet)
        result = {}
        for d, t in turnover.items():
            if t is None or t == 0:
                result[d] = None
            else:
                result[d] = 365 / t
        return result

    @staticmethod
    def receivables_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Receivables Turnover from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Receivables Turnovers with dates as keys.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If insufficient data for average calculation.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()
        if len(dates) < 2:
            raise ValueError(
                "Insufficient balance sheet data for average accounts receivable calculation."
            )

        ratios = {}
        for i in range(len(dates) - 1):
            current_period = dates[i]
            previous_period = dates[i + 1]
            try:
                revenue = income_statement.at["Total Revenue", current_period]
                receivables_end = balance_sheet.at[
                    "Accounts Receivable", current_period
                ]
                receivables_begin = balance_sheet.at[
                    "Accounts Receivable", previous_period
                ]

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
                rec_begin = to_float(
                    receivables_begin, "Accounts Receivable (beginning)"
                )

                avg_receivables = (rec_begin + rec_end) / 2
                if avg_receivables == 0:
                    ratios[current_period] = None
                else:
                    ratios[current_period] = revenue_val / avg_receivables
            except (KeyError, ValueError, TypeError):
                ratios[current_period] = None
        return ratios

    @staticmethod
    def days_of_sales_outstanding(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Days of Sales Outstanding (DSO) from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Days of Sales Outstanding (DSO) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If insufficient data for average calculation.
        """
        turnover = ActivityRatios.receivables_turnover(income_statement, balance_sheet)
        result = {}
        for d, t in turnover.items():
            if t is None or t == 0:
                result[d] = None
            else:
                result[d] = 365 / t
        return result

    @staticmethod
    def payables_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Payables Turnover from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Payables Turnovers with dates as keys.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If insufficient data for average calculation.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()
        if len(dates) < 2:
            raise ValueError(
                "Insufficient balance sheet data for average accounts payable calculation."
            )

        ratios = {}
        for i in range(len(dates) - 1):
            current_period = dates[i]
            previous_period = dates[i + 1]
            try:
                cogs = income_statement.at["Cost Of Revenue", current_period]
                payables_end = balance_sheet.at["Accounts Payable", current_period]
                payables_begin = balance_sheet.at["Accounts Payable", previous_period]

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
                    ratios[current_period] = None
                else:
                    ratios[current_period] = cogs_val / avg_payables
            except (KeyError, ValueError, TypeError):
                ratios[current_period] = None
        return ratios

    @staticmethod
    def number_of_days_of_payables(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Number of Days of Payables from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Number of Days of Payables with dates as keys.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If insufficient data for average calculation.
        """
        turnover = ActivityRatios.payables_turnover(income_statement, balance_sheet)
        result = {}
        for d, t in turnover.items():
            if t is None or t == 0:
                result[d] = None
            else:
                result[d] = 365 / t
        return result

    @staticmethod
    def working_capital_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Working Capital Turnover from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Working Capital Turnovers with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()

        ratios = {}
        for d in dates:
            try:
                revenue = income_statement.at["Total Revenue", d]
                current_assets = balance_sheet.at["Current Assets", d]
                current_liabilities = balance_sheet.at["Current Liabilities", d]

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
                    ratios[d] = None
                else:
                    ratios[d] = revenue_val / working_capital
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def fixed_asset_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Fixed Asset Turnover from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Fixed Asset Turnovers with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()

        ratios = {}
        for d in dates:
            try:
                revenue = income_statement.at["Total Revenue", d]
                net_fixed_assets = balance_sheet.at["Net PPE", d]

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
                    ratios[d] = None
                else:
                    ratios[d] = revenue_val / nfa
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def total_asset_turnover(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Total Asset Turnover from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Total Asset Turnovers with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        dates = balance_sheet.columns.tolist()

        ratios = {}
        for d in dates:
            try:
                revenue = income_statement.at["Total Revenue", d]
                total_assets = balance_sheet.at["Total Assets", d]

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
                    ratios[d] = None
                else:
                    ratios[d] = revenue_val / ta
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios
