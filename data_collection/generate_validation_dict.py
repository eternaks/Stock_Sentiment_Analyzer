import json

with open("/home/calvin/stock_predictor/data_collection/company_tickers_sec.json", mode="r", encoding="utf-8") as read_file:
    ticker_list = json.load(read_file)

ticker_map = {}

for i in range(len(ticker_list)):
    # print("generating variations for: " + ticker_list[str(i)]["ticker"])

    # create mappings
    ticker = ticker_list[str(i)]["ticker"]
    ticker_full_name = ticker_list[str(i)]["title"]

    # ticker_map[ticker] = "$" + ticker
    ticker_map["$" + ticker] = "$" + ticker
    ticker_map[ticker_full_name.upper()] = "$" + ticker
    # clean = re.match(r"^[^,\s]+", ticker_full_name)
    # ticker_map[clean.group(0).upper()] = "$" + ticker


# Ticker, Company Name short (e.g. Alphabet), Company Name Full (e.g. Alphabet Inc.), 

# dump into json
with open("/home/calvin/stock_predictor/data_collection/validation_dict_new.json", "w") as fp:
    json.dump(ticker_map, fp)