#!/usr/bin/env python3
"""
Yahoo Finance Fetcher module.
"""

import yfinance as yf
from typing import Optional
import pandas as pd


class YahooFinanceFetcher:
    """
    A class for fetching data from Yahoo Finance.
    """

    def fetch_historical_data(
        self, ticker: str, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        Fetches historical stock data from Yahoo Finance for the given ticker.

        Args:
            ticker (str): The stock ticker symbol (e.g., 'AAPL').
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame or None: The historical data as a pandas DataFrame, or None if an error occurs.
        """
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            return data
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None

    def fetch_fundamentals(self, ticker: str) -> Optional[dict]:
        """
        Fetches fundamental data from Yahoo Finance for the given ticker.

        Args:
            ticker (str): The stock ticker symbol (e.g., 'AAPL').

        Returns:
            dict or None: A dictionary containing 'info' (summary dict), 'balance_sheet' (DataFrame),
                          'income_statement' (DataFrame), 'cash_flow' (DataFrame), or None if an error occurs.
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            balance_sheet = stock.balance_sheet
            income_statement = stock.financials
            cash_flow = stock.cashflow
            return {
                "info": info,
                "balance_sheet": balance_sheet,
                "income_statement": income_statement,
                "cash_flow": cash_flow,
            }
        except Exception as e:
            print(f"Error fetching fundamentals for {ticker}: {e}")
            return None
