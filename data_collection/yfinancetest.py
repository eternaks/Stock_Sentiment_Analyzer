import yfinance as yf

dat = yf.Ticker("AAPL").info

print(dat.get("shortName"))