import yfinance as yf
import pandas as pd
from datetime import datetime

def get_s(stock: str):
    ticker = yf.Ticker(stock)
    # fast_info['lastPrice'] fetches live spot, preventing delayed 'Close' mismatches
    return ticker.history(period="1d")['Close'].iloc[-1]

def calls_list(stock: str):
    '''
    :param stock: Chosen stock for calculating Implied Volatility
    '''
    S = get_s(stock)
    ticker  = yf.Ticker(stock)
    exps = ticker.options #list of expiry date string YYYY-MM-DD
    chain = ticker.option_chain(exps[0])
    all_rows = []
    for exp in exps:
        chain = ticker.option_chain(exp)
        calls = chain.calls
        calls = calls[(calls['volume'] > 0) & (calls['bid'] > 0.0) & (calls['ask'] > 0.0)] 
        calls = calls[(calls['strike'] >= S * 0.95) & (calls['strike'] <= S * 1.1)]
        calls = calls.copy()  # avoid SettingWithCopyWarning
        calls = calls[(calls['ask'] - calls['bid']) / calls['bid'] < 0.2]#Drop options where the spread is wider than 20%

        calls['mid'] = (calls['bid'] + calls['ask']) / 2 #calculating mid (market price) instaed of using lastTradeDate
        calls['expiry'] = exp
        
        calls['T'] = calls['expiry'].apply(lambda x: time_to_expiry(x))
        calls = calls[(calls['T']) > 14.0/365.0]
        all_rows.append(calls)

    return pd.concat(all_rows, ignore_index=True)


# strike: the K for that contract
# lastPrice: price of the most recent actual trade
# bid/ask: current best quotes to buy/sell RIGHT NOW
# volume: contracts traded today
# openInterest: total contracts currently open
# impliedVolatility: IV estimate
# inTheMoney: whether K is ITM for current S

def time_to_expiry(expiry_str, calendar_days=True):
    expiry = datetime.strptime(expiry_str, "%Y-%m-%d") #convert into a number
    now = datetime.now()
    days = (expiry - now).total_seconds() / 86400  # convert n days to expire into 1/k year to expire
    return days / 365.0 if calendar_days else days / 252.0
