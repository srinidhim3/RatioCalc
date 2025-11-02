#!/usr/bin/env python3
"""
Main script for data science project.
"""

import pprint
import json
from yahoo_finance_fetcher import YahooFinanceFetcher
from liquidity_ratios import LiquidityRatios
from solvency_ratios import SolvencyRatios
from profitability_ratios import ProfitabilityRatios
from activity_ratios import ActivityRatios
from market_ratios import MarketRatios


if __name__ == "__main__":
    # Example usage
    fetcher = YahooFinanceFetcher()
    ticker = "ITC.NS"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    historical_data = fetcher.fetch_historical_data(ticker, start_date, end_date)
    if historical_data is not None:
        print(f"Historical data for {ticker}:\n", historical_data.head())

    fundamentals = fetcher.fetch_fundamentals(ticker)
    if fundamentals is not None:
        print(f"\nFundamental data for {ticker}:")
        print("Info (Summary):")
        pprint.pprint(fundamentals["info"])
        print("\nBalance Sheet (first 5 rows):")
        print(fundamentals["balance_sheet"].head())
        print("\nIncome Statement (first 5 rows):")
        print(fundamentals["income_statement"].head())
        print("\nCash Flow (first 5 rows):")
        print(fundamentals["cash_flow"].head())

        # Save fundamental data to files
        with open(f"{ticker}_info.json", "w") as f:
            json.dump(fundamentals["info"], f, indent=4)
        fundamentals["balance_sheet"].to_csv(f"{ticker}_balance_sheet.csv")
        fundamentals["income_statement"].to_csv(f"{ticker}_income_statement.csv")
        fundamentals["cash_flow"].to_csv(f"{ticker}_cash_flow.csv")
        print(
            f"\nFundamental data saved to {ticker}_info.json, {ticker}_balance_sheet.csv, {ticker}_income_statement.csv, and {ticker}_cash_flow.csv"
        )

        # Calculate ratios
        latest_date = fundamentals["balance_sheet"].columns[0]
        # Calculate Current Ratio (liquidity ratios)
        try:
            current_ratio = LiquidityRatios.current_ratio(fundamentals["balance_sheet"])
            print(
                f"\nCalculated Current Ratio for {ticker} ({latest_date}): {current_ratio:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Current Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Current Ratio: {e}")

        # Calculate Quick Ratio
        try:
            quick_ratio = LiquidityRatios.quick_ratio(fundamentals["balance_sheet"])
            print(
                f"Calculated Quick Ratio for {ticker} ({latest_date}): {quick_ratio:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Quick Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Quick Ratio: {e}")

        # Calculate Cash Ratio
        try:
            cash_ratio = LiquidityRatios.cash_ratio(fundamentals["balance_sheet"])
            print(
                f"Calculated Cash Ratio for {ticker} ({latest_date}): {cash_ratio:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Cash Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Cash Ratio: {e}")

        # Calculate Debt-to-Assets Ratio (next ratio to be calculated)
        try:
            debt_to_assets = SolvencyRatios.debt_to_assets_ratio(
                fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Debt-to-Assets Ratio for {ticker} ({latest_date}): {debt_to_assets:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Debt-to-Assets Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Debt-to-Assets Ratio: {e}")

        # Calculate Debt-to-Equity Ratio from info
        try:
            debt_to_equity = SolvencyRatios.debt_to_equity_ratio_from_info(
                fundamentals["info"]
            )
            print(
                f"Debt-to-Equity Ratio for {ticker} (from Yahoo Finance): {debt_to_equity:.6f}"
            )
        except KeyError as e:
            print(f"Error retrieving Debt-to-Equity Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Debt-to-Equity Ratio: {e}")

        # Calculate Financial Leverage Ratio
        try:
            financial_leverage = SolvencyRatios.financial_leverage_ratio(
                fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Financial Leverage Ratio for {ticker} ({latest_date}): {financial_leverage:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Financial Leverage Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Financial Leverage Ratio: {e}")

        # Calculate Interest Coverage Ratio
        try:
            interest_coverage = SolvencyRatios.interest_coverage_ratio(
                fundamentals["income_statement"]
            )
            print(
                f"Calculated Interest Coverage Ratio for {ticker} ({latest_date}): {interest_coverage:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Interest Coverage Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Interest Coverage Ratio: {e}")

        # Calculate Return on Assets (ROA)
        try:
            roa = ProfitabilityRatios.return_on_assets(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Return on Assets (ROA) for {ticker} ({latest_date}): {roa:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Return on Assets (ROA): Missing key {e}")
        except Exception as e:
            print(f"Error calculating Return on Assets (ROA): {e}")

        # Calculate Return on Equity (ROE)
        try:
            roe = ProfitabilityRatios.return_on_equity(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Return on Equity (ROE) for {ticker} ({latest_date}): {roe:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Return on Equity (ROE): Missing key {e}")
        except Exception as e:
            print(f"Error calculating Return on Equity (ROE): {e}")

        # Calculate Return on Total Capital (ROTC)
        try:
            rotc = ProfitabilityRatios.return_on_total_capital(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Return on Total Capital (ROTC) for {ticker} ({latest_date}): {rotc:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Return on Total Capital (ROTC): Missing key {e}")
        except Exception as e:
            print(f"Error calculating Return on Total Capital (ROTC): {e}")
        # Calculate Return on Common Equity (ROCE)
        try:
            roce = ProfitabilityRatios.return_on_common_equity(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Return on Common Equity (ROCE) for {ticker} ({latest_date}): {roce:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Return on Common Equity (ROCE): Missing key {e}")
        except Exception as e:
            print(f"Error calculating Return on Common Equity (ROCE): {e}")
        try:
            dir_ratio = LiquidityRatios.defensive_interval_ratio(
                fundamentals["balance_sheet"], fundamentals["income_statement"]
            )
            print(
                f"Calculated Defensive Interval Ratio for {ticker} ({latest_date}): {dir_ratio:.6f} days"
            )
        except KeyError as e:
            print(f"Error calculating Defensive Interval Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Defensive Interval Ratio: {e}")

        # Calculate Inventory Turnover
        try:
            inventory_turnover = ActivityRatios.inventory_turnover(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Inventory Turnover for {ticker} ({latest_date}): {inventory_turnover:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Inventory Turnover: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Inventory Turnover: {e}")

        # Calculate Days of Inventory on Hand (DOH)
        try:
            doh = ActivityRatios.days_of_inventory_on_hand(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Days of Inventory on Hand (DOH) for {ticker} ({latest_date}): {doh:.6f} days"
            )
        except KeyError as e:
            print(f"Error calculating Days of Inventory on Hand (DOH): Missing key {e}")
        except Exception as e:
            print(f"Error calculating Days of Inventory on Hand (DOH): {e}")

        # Calculate Receivables Turnover
        try:
            receivables_turnover = ActivityRatios.receivables_turnover(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Receivables Turnover for {ticker} ({latest_date}): {receivables_turnover:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Receivables Turnover: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Receivables Turnover: {e}")

        # Calculate Days of Sales Outstanding (DSO)
        try:
            dso = ActivityRatios.days_of_sales_outstanding(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Days of Sales Outstanding (DSO) for {ticker} ({latest_date}): {dso:.6f} days"
            )
        except KeyError as e:
            print(f"Error calculating Days of Sales Outstanding (DSO): Missing key {e}")
        except Exception as e:
            print(f"Error calculating Days of Sales Outstanding (DSO): {e}")

        # Calculate Payables Turnover
        try:
            payables_turnover = ActivityRatios.payables_turnover(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Payables Turnover for {ticker} ({latest_date}): {payables_turnover:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Payables Turnover: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Payables Turnover: {e}")

        # Calculate Number of Days of Payables
        try:
            days_payables = ActivityRatios.number_of_days_of_payables(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Number of Days of Payables for {ticker} ({latest_date}): {days_payables:.6f} days"
            )
        except KeyError as e:
            print(f"Error calculating Number of Days of Payables: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Number of Days of Payables: {e}")

        # Calculate Working Capital Turnover
        try:
            wc_turnover = ActivityRatios.working_capital_turnover(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Working Capital Turnover for {ticker} ({latest_date}): {wc_turnover:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Working Capital Turnover: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Working Capital Turnover: {e}")

        # Calculate Fixed Asset Turnover
        try:
            fa_turnover = ActivityRatios.fixed_asset_turnover(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Fixed Asset Turnover for {ticker} ({latest_date}): {fa_turnover:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Fixed Asset Turnover: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Fixed Asset Turnover: {e}")

        # Calculate Total Asset Turnover
        try:
            ta_turnover = ActivityRatios.total_asset_turnover(
                fundamentals["income_statement"], fundamentals["balance_sheet"]
            )
            print(
                f"Calculated Total Asset Turnover for {ticker} ({latest_date}): {ta_turnover:.6f}"
            )
        except KeyError as e:
            print(f"Error calculating Total Asset Turnover: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Total Asset Turnover: {e}")

        # Calculate Price-to-Cash Flow Ratio from info
        try:
            ptcf_ratio = MarketRatios.price_to_cash_flow_ratio(fundamentals["info"])
            print(f"Calculated Price-to-Cash Flow Ratio for {ticker}: {ptcf_ratio:.6f}")
        except KeyError as e:
            print(f"Error calculating Price-to-Cash Flow Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Price-to-Cash Flow Ratio: {e}")

        # Calculate Retention Rate from info
        try:
            retention_rate = MarketRatios.retention_rate(fundamentals["info"])
            print(f"Calculated Retention Rate for {ticker}: {retention_rate:.6f}")
        except KeyError as e:
            print(f"Error calculating Retention Rate: Missing key {e}")
        except Exception as e:
            print(f"Error calculating Retention Rate: {e}")

        # Yahoo Finance Ratios
        print(f"\nYahoo Finance Ratios for {ticker}:")

        # Profitability Ratios from Yahoo Finance
        try:
            gross_margin = ProfitabilityRatios.gross_profit_margin_from_info(
                fundamentals["info"]
            )
            print(f"Gross Profit Margin: {gross_margin:.6f}")
        except KeyError as e:
            print(f"Error retrieving Gross Profit Margin: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Gross Profit Margin: {e}")

        try:
            operating_margin = ProfitabilityRatios.operating_profit_margin_from_info(
                fundamentals["info"]
            )
            print(f"Operating Profit Margin: {operating_margin:.6f}")
        except KeyError as e:
            print(f"Error retrieving Operating Profit Margin: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Operating Profit Margin: {e}")

        try:
            net_margin = ProfitabilityRatios.net_profit_margin_from_info(
                fundamentals["info"]
            )
            print(f"Net Profit Margin: {net_margin:.6f}")
        except KeyError as e:
            print(f"Error retrieving Net Profit Margin: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Net Profit Margin: {e}")

        # Market Ratios from Yahoo Finance
        try:
            pe_ratio = MarketRatios.price_to_earnings_ratio_from_info(
                fundamentals["info"]
            )
            print(f"Price-to-Earnings Ratio: {pe_ratio:.6f}")
        except KeyError as e:
            print(f"Error retrieving Price-to-Earnings Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Price-to-Earnings Ratio: {e}")

        try:
            pb_ratio = MarketRatios.price_to_book_ratio_from_info(fundamentals["info"])
            print(f"Price-to-Book Ratio: {pb_ratio:.6f}")
        except KeyError as e:
            print(f"Error retrieving Price-to-Book Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Price-to-Book Ratio: {e}")

        try:
            ps_ratio = MarketRatios.price_to_sales_ratio_from_info(fundamentals["info"])
            print(f"Price-to-Sales Ratio: {ps_ratio:.6f}")
        except KeyError as e:
            print(f"Error retrieving Price-to-Sales Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Price-to-Sales Ratio: {e}")

        try:
            div_yield = MarketRatios.dividend_yield_from_info(fundamentals["info"])
            print(f"Dividend Yield: {div_yield:.6f}")
        except KeyError as e:
            print(f"Error retrieving Dividend Yield: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Dividend Yield: {e}")

        try:
            div_payout = MarketRatios.dividend_payout_ratio_from_info(
                fundamentals["info"]
            )
            print(f"Dividend Payout Ratio: {div_payout:.6f}")
        except KeyError as e:
            print(f"Error retrieving Dividend Payout Ratio: Missing key {e}")
        except Exception as e:
            print(f"Error retrieving Dividend Payout Ratio: {e}")

        # DuPont Analysis
        print(f"\nDuPont Analysis for {ticker}:")
        try:
            dupont = ProfitabilityRatios.dupont_analysis(
                fundamentals["income_statement"],
                fundamentals["balance_sheet"],
                fundamentals["info"],
            )
            print(f"ROE: {dupont['roe']:.6f}")
            print(f"Net Profit Margin: {dupont['net_profit_margin']:.6f}")
            print(f"Asset Turnover: {dupont['asset_turnover']:.6f}")
            print(f"Financial Leverage: {dupont['financial_leverage']:.6f}")
            # Verify: ROE should equal NPM × AT × FL
            calculated_roe = (
                dupont["net_profit_margin"]
                * dupont["asset_turnover"]
                * dupont["financial_leverage"]
            )
            print(f"Calculated ROE (NPM × AT × FL): {calculated_roe:.6f}")
        except KeyError as e:
            print(f"Error performing DuPont Analysis: Missing key {e}")
        except Exception as e:
            print(f"Error performing DuPont Analysis: {e}")
