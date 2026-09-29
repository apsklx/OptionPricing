import yfinance as yf
import pandas as pd
ticker = yf.Ticker("AAPL")
S = ticker.history(period="1d")['Close'].iloc[-1]
exps = ticker.options #list of expiry date string YYYY-MM-DD

chain = ticker.option_chain(exps[0])

all_rows = []
for exp in exps:
    chain = ticker.option_chain(exp)
    calls = chain.calls
    calls = calls[(calls['volume'] > 0) & (calls['bid'] > 0.0) & (calls['ask'] > 0.0)] # filter data
    calls = calls.copy()  # avoid SettingWithCopyWarning
    calls['mid'] = (calls['bid'] + calls['ask']) / 2 #calculating mid instaed of using lastTradeDate
    calls['expiry'] = exp
    all_rows.append(calls)
full_calls = pd.concat(all_rows, ignore_index=True)
print(full_calls['mid'])