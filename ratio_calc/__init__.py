"""
RatioCalc - A comprehensive financial ratios calculator.

This package provides tools for calculating financial ratios from Yahoo Finance data,
including liquidity, solvency, profitability, activity ratios, and DuPont analysis.
"""

from .calculator import FinancialRatioCalculator
from .yahoo_finance_fetcher import YahooFinanceFetcher

__version__ = "1.1.0"
__author__ = "srinidhim3"
__email__ = ""  # Add your email here

__all__ = [
    "FinancialRatioCalculator",
    "YahooFinanceFetcher",
]
