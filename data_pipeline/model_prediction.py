from pyabsa import AspectTermExtraction as ATEPC, available_checkpoints
from pyabsa import TaskCodeOption
import re
import json
import database

aspect_extractor = ATEPC.AspectExtractor('data_pipeline/rddt_.7_FINAL_checkpt',
                                         auto_device=True,  # False means load model on CPU
                                         cal_perplexity=True,
                                         verbose=True
                                         )

with open("data_pipeline/validation_dict.json", mode="r", encoding="utf-8") as read_file:
    valid = json.load(read_file)

def predict(submission):
    prediction = aspect_extractor.predict([submission],
                         save_result=False,
                         print_result=False,  # print the result
                         ignore_error=True,  # ignore the error when the model cannot predict the input
                         )
    ticker_list = prediction[0]["aspect"]
    sentiment_list = prediction[0]["sentiment"]
    confidence_list = prediction[0]["confidence"]
    # loop through ticker list, extract corresponding terms, then match with corresponding sentiment and confidence
    i = 0
    for ticker in ticker_list:
        matches = re.findall(r'\$\s*([a-zA-Z_][a-zA-Z0-9_]*)', ticker)
        for match in matches:
            if "$" + match in valid:
                database.insert("$" + match, sentiment_list[i], str(confidence_list[i]))
        i+=1
    