#!/usr/bin/env python3
"""
Setup script for RatioCalc package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ratio-calc",
    version="1.1.0",
    author="srinidhim3",
    author_email="your.email@example.com",
    description="A comprehensive financial ratios calculator for Yahoo Finance data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/srinidhim3/RatioCalc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    keywords="finance ratios yahoo-finance analysis cfa",
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "yfinance>=0.1.70",
    ],
    entry_points={
        "console_scripts": [
            "ratio-calc=ratio_calc.calculator:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
