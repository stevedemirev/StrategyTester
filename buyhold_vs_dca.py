import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import time

class Backtest:
    def __init__(self,market_data):
        self.investment = 100000
        self.closing_prices = market_data['Adj Close']
        
    def buy_hold_strategy(self):
        first = self.closing_prices.iloc[0]
        last = self.closing_prices.iloc[-1]
        buy_hold_ror = ((last-first)/first)
        buy_hold_fv = (1+buy_hold_ror) * self.investment
        return buy_hold_ror*100, buy_hold_fv
    
    def dollar_cost_averaging_strategy(self):
        daily_purchase = self.investment/len(self.closing_prices)
        shares = 0
        for price in self.closing_prices:
            shares_bought = daily_purchase/price
            shares += shares_bought
        dca_fv = shares * self.closing_prices.iloc[-1]
        dca_ror = ((dca_fv- self.investment)/self.investment)*100
        return dca_ror, dca_fv
    
    def custom_strategy(self):
        daily_purchase = self.investment/len(self.closing_prices)
        shares = 0
        prev_price = self.closing_prices.iloc[0]
        count = 1
        for price in self.closing_prices[1:]:
            pct_change = ((price - prev_price)/price)*100
        #    print(pct_change)
            if pct_change < 0 :
                shares_bought = (count)*(daily_purchase/price)
                shares += shares_bought
                count = 1
            else:
                count+=1
            prev_price = price
        strat_fv = shares* self.closing_prices.iloc[-1]
        strat_ror = ((strat_fv - self.investment)/self.investment)*100
        return strat_ror, strat_fv
    
    def run_all(self):
        bh_ror, bh_fv = self.buy_hold_strategy()
        dca_ror, dca_fv = self.dollar_cost_averaging_strategy()
        cust_ror, cust_fv = self.custom_strategy()
        print(f"Initial Investment: ${self.investment:,.2f}")
        print(f"B&H RoR: {bh_ror:.2f}% ; B&H Final Value: ${bh_fv:,.2f}\n")
        print(f"DCA RoR: {dca_ror:.2f}% ; DCA Final Value: ${dca_fv:,.2f}\n")
        print(f"Custom Strategy RoR: {cust_ror:.2f}% ; Custom Strategy Final Value: ${cust_fv:,.2f}")
        

def count_strategies(tickers,start,end):
    t_count = 0
    bh_count = 0
    dca_count = 0
    cust_count = 0
    for i,ticker in enumerate(tickers):
        ticker = ticker.replace('.','-')
        total_tickers = len(tickers)
        begin_time=time.time()
        progress = (i+1)/total_tickers*100
        elapsed_time = time.time() - begin_time
        eta = (elapsed_time / progress) * (100 - progress)
        eta_str = time.strftime('%H:%M:%S', time.gmtime(eta))
        print(f"\rProgress: '${ticker}' {progress:.2f}% ETA: {eta_str}", end='', flush=True)
        df = yf.download(ticker,start,end,progress=False)
        bt = Backtest(df)
        bh_ror,bh_fv = bt.buy_hold_strategy()
        dca_ror,dca_fv = bt.dollar_cost_averaging_strategy()
        cust_ror,cust_fv = bt.custom_strategy()
        t_count+=1
        if bh_ror > dca_ror and bh_ror > cust_ror:
            bh_count+=1
        elif dca_ror > bh_ror and dca_ror > cust_ror:
            dca_count+=1
        elif cust_ror > bh_ror and cust_ror > dca_ror:
            cust_count +=1
        else:
        # Handle ties, if necessary
            if bh_ror == dca_ror and bh_ror == cust_ror:
                bh_count += 1
                dca_count += 1
                cust_count += 1
            elif bh_ror == dca_ror:
                bh_count += 1
                dca_count += 1
            elif bh_ror == cust_ror:
                bh_count += 1
                cust_count += 1
            elif dca_ror == cust_ror:
                dca_count += 1
                cust_count += 1
    print("Total Count: ", t_count)
    print(f"B&H Count: {bh_count}; Percentage won: {(bh_count/t_count):.2f}%")
    print(f"DCA Count: {dca_count}; Percentage won: {(dca_count/t_count):.2f}%")
    print(f"Custom Strategy Count: {cust_count}; Percentage won: {(cust_count/t_count):.2f}%")

def read_company_tickers():
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    return df['Symbol'].to_list()
        
def main():
    choice = input("Enter 1 for SPY; Enter 2 for a specific ticker; Enter 3 for entire S&P 500; Anything else to quit: ")
    if choice == "1":
        years = int(input(f"Please enter the number of years to backtest from: "))
        end_date = datetime.date.today()
        time_delta = datetime.timedelta(days=years*365.25)
        start_date = end_date - time_delta
        data = yf.download("SPY",start_date,end_date)
        bt = Backtest(data)
        bt.run_all()
    elif choice == "2":
        ticker = input("Enter a ticker: ")
        years = int(input(f"Please enter the number of years to backtest from: "))
        end_date = datetime.date.today()
        time_delta = datetime.timedelta(days=years*365.25)
        start_date = end_date - time_delta
        data = yf.download(ticker,start_date,end_date)
        bt = Backtest(data)
        bt.run_all()
    elif choice == "3":
        years = int(input(f"Please enter the number of years to backtest from: "))
        end_date = datetime.date.today()
        time_delta = datetime.timedelta(days=years*365.25)
        start_date = end_date - time_delta
       # bt = Backtest()
        tickers = read_company_tickers()
        count_strategies(tickers,start_date,end_date)
    else:
        quit()

if __name__ == "__main__":
    main()
    
# Code below was modified 
"""    end_date = datetime.date.today()
    time_delta = datetime.timedelta(days=20*365.25) # Modify coefficient to be input if you want
    start_date = end_date - time_delta
    


    tickers = read_company_tickers()
    count_strategies(tickers,start_date,end_date)
    #print(f"B&H RoR: {bh_ror} ; B&H Final Value: {bh_fv}\n")
    #print(f"DCA RoR: {dca_ror} ; DCA Final Value: {dca_fv}\n")
    #print(f"Custom Strategy RoR: {cust_ror} ; Custom Strategy Final Value: {cust_fv}")"""
    

   
# Original Implementation     
"""
### Get Data from YFinance
#ticker = input("Input ticker: ")
ticker = "SPY"
# start_date = input("Input starting date: ")
start_date = "2004-05-27"
end_date = datetime.date.today()
investment = 100000
spy_df = yf.download(ticker,start_date,end_date)

### Get Adjusted_close Dataframe
adj_close = spy_df['Adj Close']

### Buy&Hold Strategy
first = adj_close.iloc[0]
last = adj_close.iloc[-1]
buy_hold_rate_of_return = ((last-first)/first)
buy_hold_total_val = buy_hold_rate_of_return * investment

### DCA Strategy
daily_purchase = investment/len(adj_close)
shares = 0
for price in adj_close:
    shares_bought = daily_purchase/price
    shares += shares_bought
    
dca_total_val = shares * adj_close.iloc[-1]
dca_ror = ((dca_total_val-investment)/investment)*100

### Custom Strategy
new_investment = 100000
daily_purchase = new_investment/len(adj_close)
shares = 0
prev_price = 0
count = 1
for price in adj_close:
    pct_change = ((price - prev_price)/price)*100
#    print(pct_change)
    if pct_change < 0 :
        shares_bought = (count)*(daily_purchase/price)
        shares += shares_bought
        count = 1
    else:
        count+=1
    prev_price = price

print(count ,"\n")
strat_val = shares* adj_close.iloc[-1]
strat_ror = ((strat_val - new_investment)/new_investment)*100
        
    

### Print results
print(f"Buy & Hold Rate of Return: {buy_hold_rate_of_return*100} %")
print(f"Buy & Hold Total Value: $ {buy_hold_total_val} \n")
print(f"DCA Rate of Return: {dca_ror} %")
print(f"DCA Total Value: $ {dca_total_val} \n")
print(f"Custom Strategy Rate of Return: {strat_ror} %")
print(f"Custom Strategy Total Value: $ {strat_val}")"""

##### Results:
# Varies between stock to stock. Higher performing stocks will do better B&H; 
# While Worse performing stocks will produce better results with DCA.
# Stocks that dip generally will do better with DCA (i.e Coinbase $COIN, Bitcoin Miners $MARA,$HUT,$BITF)
