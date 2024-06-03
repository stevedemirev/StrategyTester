# StrategyTester
Simple Backtesting program

This program uses financial data from Yahoo! Finance in order to simulate the rate of return and total return from $100,000 using a given strategy.

### Purpose:
The purpose of this program is to view the rate of return from specific strategies. 
The strategies tested in this program are a Lump-sum investment of $100,000 (Buy and Hold), a Dollar-Cost-Averaging investment strategy of $100,000 spread evenly between the numbers of days tested, and a custom strategy which you can implement to view the rate of return using $100,000.


### How To Use:
First install the dependencies used: 
  - Numpy
  - Pandas
  - YFinance
  - Datetime
  - Time

If using Linux, use the following commands:
```sh
  python3 -m pip install numpy
  python3 -m pip install pandas
  python3 -m pip install yfinance
  python3 -m pip install datetime
  python3 -m pip install time
```

Once the program is running, select an option given:
    *1: Backtest strategies using Historical Financial Data for the S&P 500 ($SPY)
    *2: Backtest strategies using Historical Financial Data for a specific stock you input (i.e $MSFT, $AAPL, $TSLA)
    *3: View the comparative results of each strategy tested against the others using data from each individual stock from the S&P 500.

  Next input how far back your backtest will be:
    *End date will always be today
    *Start date will be based in years before current day.

I hope you find this program somewhat interesting. Please be sure to comment any errors, miscalculations, or bugs.
Thank you!
