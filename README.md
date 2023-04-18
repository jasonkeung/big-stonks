# big-stonks

This is a stocks/trading backtesting software built from scratch using Python and data from Yahoo Finance. Algorithms are defined in *trader.py files and use a framework defined by ticker, trader, and order classes. Tests are written in backtest.py to run an algorithm over a desired set of ticker symbols over a period of time, and performance metrics like alpha can be calculated and displayed.

## Installation and Usage

Install the Yahoo finance python package

    pip3 install yfinance
Write your own tests in backtest.py according to the documentation in related files such as trader.py and ticker.py

Run your tests using
 
    python3 backtest.py
