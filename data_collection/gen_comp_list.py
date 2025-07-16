import json

with open("/home/calvin/stock_predictor/data_collection/company_tickers_sec.json", mode="r", encoding="utf-8") as read_file:
    ticker_list = json.load(read_file)

