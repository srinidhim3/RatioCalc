#!/usr/bin/env python3
"""
Market Ratios Calculator module.
"""

from typing import Dict, Any
import pandas as pd


class MarketRatios:
    """
    A class for calculating market (valuation) ratios from financial statements and market data.
    """

    @staticmethod
    def price_to_cash_flow_ratio(info: Dict[str, Any]) -> float:
        """
        Calculates the Price-to-Cash Flow Ratio from the company info.

        Formula: Market Price per Share / Cash Flow per Share
        Where Cash Flow per Share = Operating Cash Flow / Shares Outstanding

        Args:
            info (dict): The company info dictionary from Yahoo Finance.

        Returns:
            float: The Price-to-Cash Flow Ratio.

        Raises:
            KeyError: If required keys are missing from info.
            ZeroDivisionError: If shares outstanding or cash flow per share is zero.
            ValueError: If data is invalid.
        """
        if info is None:
            raise ValueError("Company info data is None.")

        try:
            market_price = info["currentPrice"]
            operating_cash_flow = info["operatingCashflow"]
            shares_outstanding = info["sharesOutstanding"]
        except KeyError as e:
            raise KeyError(f"Required key missing from info: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        market_price_val = to_float(market_price, "currentPrice")
        ocf_val = to_float(operating_cash_flow, "operatingCashflow")
        shares_val = to_float(shares_outstanding, "sharesOutstanding")

        if shares_val == 0:
            raise ZeroDivisionError("Shares outstanding is zero.")

        cash_flow_per_share = ocf_val / shares_val

        if cash_flow_per_share == 0:
            raise ZeroDivisionError("Cash flow per share is zero.")

        return market_price_val / cash_flow_per_share

    @staticmethod
    def retention_rate(info: Dict[str, Any]) -> float:
        """
        Calculates the Retention Rate from the company info.

        Formula: 1 - Dividend Payout Ratio

        Args:
            info (dict): The company info dictionary from Yahoo Finance.

        Returns:
            float: The Retention Rate.

        Raises:
            KeyError: If required keys are missing from info.
            ValueError: If data is invalid.
        """
        if info is None:
            raise ValueError("Company info data is None.")

        try:
            payout_ratio = info["payoutRatio"]
        except KeyError as e:
            raise KeyError(f"Required key missing from info: {e}")

        def to_float(val, name: str) -> float:
            if pd.isna(val):
                raise ValueError(f"{name} is NaN or missing")
            if isinstance(val, complex):
                raise TypeError(
                    f"{name} is a complex number and cannot be converted to float"
                )
            return float(val)

        payout_val = to_float(payout_ratio, "payoutRatio")

        return 1 - payout_val
