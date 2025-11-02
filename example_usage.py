#!/usr/bin/env python3
"""
Example usage of the FinancialRatioCalculator class.
"""

from main import FinancialRatioCalculator


def main():
    # Example 1: Basic usage
    print("=== Example 1: Basic Usage ===")
    calculator = FinancialRatioCalculator(
        ticker="ITC.NS",
        drop_periods=["2021-03-31"],  # Skip problematic periods
    )
    df_ratios = calculator.run(save_csv=True, verbose=True)

    # Example 2: Programmatic analysis
    print("\n=== Example 2: Programmatic Analysis ===")
    print(f"DataFrame shape: {df_ratios.shape}")
    print(f"Total ratios calculated: {len(df_ratios.index)}")
    print(f"Total periods analyzed: {len(df_ratios.columns)}")

    # Get current ratio trend
    try:
        current_ratio = df_ratios.loc["Current Ratio"]
        print(f"Current Ratio trend: {current_ratio.values}")
    except KeyError:
        print("Current Ratio not found in results")
        print(f"Available ratios: {list(df_ratios.index)[:5]}...")

    # Find ratios with most variation
    ratio_variation = df_ratios.std(axis=1).sort_values(ascending=False)
    print("\nRatios with highest variation:")
    print(ratio_variation.head(5))

    # Example 3: Custom analysis for specific ratios
    print("\n=== Example 3: Custom Analysis ===")
    try:
        roe_ratios = df_ratios.loc[["Return on Equity (ROE)", "DuPont ROE"]]
        print("ROE Comparison:")
        print(roe_ratios)
    except KeyError as e:
        print(f"Error accessing ROE ratios: {e}")
        print(f"Available ratios: {list(df_ratios.index)}")


if __name__ == "__main__":
    main()
