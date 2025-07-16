import json
import re

with open("/home/calvin/stock_predictor/data_collection/validation_dict_FINAL.json", mode="r", encoding="utf-8") as read_file:
    valid = json.load(read_file)

def validate(post):
    has_ticker = False
    ptr1 = 0
    i = 0
    out = ""
    while i <= len(post):
        word = ""
        if i == len(post) or post[i] == " " or post[i] == "," or post[i] == "." or post[i] == ")" or post[i] == "(":
            word = post[ptr1:i]
            if word != "" and word[0] == '$':
                word = word.upper()
            if word in valid:
                word = valid[word]
                has_ticker = True
            ptr1 = i+1
            out += word
            if i != len(post):
                out += post[i]
        i+=1
    return (out, has_ticker)

regex_pattern = r'https:\S*|!\[img\]\(emote\|\S*'

def clean_data(var1):
    if "⣿" in var1:
        return ''
    if "This post contains content not supported on old Reddit. [Click here to view the full post](" in var1:
        return ''
    if "[ Removed by Reddit ]" in var1 or "[removed]" in var1 or "[deleted]" in var1 or "This was written by ChatGPT" in var1 or "#Ban" in var1 or "!banbet" in var1:
        return ''
    var1 = re.sub(regex_pattern, '', var1)
    var1 = re.sub(r'\n[\n ]*', '. ', var1)
    return var1