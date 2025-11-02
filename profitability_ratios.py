#!/usr/bin/env python3
"""
Profitability Ratios Calculator module.
"""

from typing import Optional, Dict, Any
import pandas as pd


class ProfitabilityRatios:
    """
    A class for calculating profitability ratios from financial statements.
    """

    @staticmethod
    def return_on_assets(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Return on Assets (ROA) from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Return on Assets (ROA) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                net_income = income_statement.at[
                    "Net Income From Continuing Operation Net Minority Interest", d
                ]
                total_assets = balance_sheet.at["Total Assets", d]

                def to_float(val, name: str) -> float:
                    if pd.isna(val):
                        raise ValueError(f"{name} is NaN or missing")
                    if isinstance(val, complex):
                        raise TypeError(
                            f"{name} is a complex number and cannot be converted to float"
                        )
                    return float(val)

                net_inc = to_float(
                    net_income,
                    "Net Income From Continuing Operation Net Minority Interest",
                )
                assets = to_float(total_assets, "Total Assets")

                if assets == 0:
                    ratios[d] = None
                else:
                    ratios[d] = net_inc / assets
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def return_on_equity(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Return on Equity (ROE) from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Return on Equity (ROE) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                net_income = income_statement.at[
                    "Net Income From Continuing Operation Net Minority Interest", d
                ]
                shareholders_equity = balance_sheet.at[
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

                net_inc = to_float(
                    net_income,
                    "Net Income From Continuing Operation Net Minority Interest",
                )
                equity = to_float(
                    shareholders_equity, "Total Equity Gross Minority Interest"
                )

                if equity == 0:
                    ratios[d] = None
                else:
                    ratios[d] = net_inc / equity
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def return_on_total_capital(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Return on Total Capital (ROTC) from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Return on Total Capital (ROTC) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                ebit = income_statement.at["EBIT", d]
                total_debt = balance_sheet.at["Total Debt", d]
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

                ebit_val = to_float(ebit, "EBIT")
                debt = to_float(total_debt, "Total Debt")
                equity = to_float(total_equity, "Total Equity Gross Minority Interest")

                total_capital = debt + equity
                if total_capital == 0:
                    ratios[d] = None
                else:
                    ratios[d] = ebit_val / total_capital
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def return_on_common_equity(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
    ) -> Dict[str, Optional[float]]:
        """
        Calculates the Return on Common Equity (ROCE) from the income statement and balance sheet for all available periods.

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.

        Returns:
            dict: The Return on Common Equity (ROCE) with dates as keys.

        Raises:
            KeyError: If required keys are missing.
        """
        if income_statement is None or balance_sheet is None:
            raise ValueError("Income statement or balance sheet data is None.")

        ratios = {}
        for d in balance_sheet.columns:
            try:
                net_income = income_statement.at[
                    "Net Income From Continuing Operation Net Minority Interest", d
                ]
                common_equity = balance_sheet.at[
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

                net_inc = to_float(
                    net_income,
                    "Net Income From Continuing Operation Net Minority Interest",
                )
                equity = to_float(common_equity, "Total Equity Gross Minority Interest")

                if equity == 0:
                    ratios[d] = None
                else:
                    ratios[d] = net_inc / equity
            except (KeyError, ValueError, TypeError):
                ratios[d] = None
        return ratios

    @staticmethod
    def gross_profit_margin_from_info(info: Dict[str, Any]) -> float:
        """
        Get Gross Profit Margin from Yahoo Finance info.

        Args:
            info (dict): The company info dictionary from Yahoo Finance.

        Returns:
            float: The Gross Profit Margin.

        Raises:
            KeyError: If grossMargins is not found in info.
        """
        try:
            return info["grossMargins"]
        except KeyError:
            raise KeyError("grossMargins not found in info")

    @staticmethod
    def operating_profit_margin_from_info(info: Dict[str, Any]) -> float:
        """
        Get Operating Profit Margin from Yahoo Finance info.

        Args:
            info (dict): The company info dictionary from Yahoo Finance.

        Returns:
            float: The Operating Profit Margin.

        Raises:
            KeyError: If operatingMargins is not found in info.
        """
        try:
            return info["operatingMargins"]
        except KeyError:
            raise KeyError("operatingMargins not found in info")

    @staticmethod
    def net_profit_margin_from_info(info: Dict[str, Any]) -> float:
        """
        Get Net Profit Margin from Yahoo Finance info.

        Args:
            info (dict): The company info dictionary from Yahoo Finance.

        Returns:
            float: The Net Profit Margin.

        Raises:
            KeyError: If profitMargins is not found in info.
        """
        try:
            return info["profitMargins"]
        except KeyError:
            raise KeyError("profitMargins not found in info")

    @staticmethod
    def dupont_analysis(
        income_statement: pd.DataFrame,
        balance_sheet: pd.DataFrame,
        info: Dict[str, Any],
    ) -> Dict[str, Dict[str, Optional[float]]]:
        """
        Performs DuPont Analysis to break down ROE into its components for all available periods.

        ROE = Net Profit Margin × Total Asset Turnover × Financial Leverage

        Args:
            income_statement (pd.DataFrame): The income statement DataFrame.
            balance_sheet (pd.DataFrame): The balance sheet DataFrame.
            info (dict): The company info dictionary from Yahoo Finance.

        Returns:
            dict: A dictionary with dates as keys containing component dicts.

        Raises:
            KeyError: If required keys are missing.
            ValueError: If data is invalid.
        """
        # Calculate Net Profit Margin
        try:
            net_profit_margin = info["profitMargins"]
        except KeyError:
            raise KeyError("profitMargins not found in info")

        # Calculate Total Asset Turnover
        from activity_ratios import ActivityRatios

        asset_turnover = ActivityRatios.total_asset_turnover(
            income_statement, balance_sheet
        )

        # Calculate Financial Leverage
        from solvency_ratios import SolvencyRatios

        leverage = SolvencyRatios.financial_leverage_ratio(balance_sheet)

        # Calculate ROE
        roe = ProfitabilityRatios.return_on_equity(income_statement, balance_sheet)

        result = {}
        for d in balance_sheet.columns:
            result[d] = {
                "roe": roe.get(d),
                "net_profit_margin": net_profit_margin,
                "asset_turnover": asset_turnover.get(d),
                "financial_leverage": leverage.get(d),
            }
        return result
