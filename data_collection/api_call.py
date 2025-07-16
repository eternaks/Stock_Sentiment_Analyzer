import praw
from praw.models import MoreComments
from dotenv import load_dotenv
import os
import pandas as pd
import data_preprocessing

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    user_agent = os.getenv('user_agent')
)

postcnt = 0
commentcnt = 0

data = []

print("Beginning Scraping")

for submission in reddit.subreddit("wallstreetbets").hot(limit=None):
    sub_titletxt = data_preprocessing.clean_data(submission.selftext)
    sub_titletxt = data_preprocessing.validate(sub_titletxt)
    if sub_titletxt[1]:
        data.append(sub_titletxt[0])
        postcnt += 1

    # add title to dataset
    sub_title = data_preprocessing.clean_data(submission.title)
    sub_title = data_preprocessing.validate(sub_title)
    if sub_title[1]:
        data.append(sub_title[0])
        postcnt += 1

    firstcmt = True

    # process comments
    for top_level_comment in submission.comments:
        # ignore bot comment
        if firstcmt:
            firstcmt = False
            continue
        
        # prevent weird bug with api
        if isinstance(top_level_comment, MoreComments):
            continue

        # more data cleaning
        com_body = data_preprocessing.clean_data(top_level_comment.body)
        com_body = data_preprocessing.validate(com_body)
        if com_body[1]:
            commentcnt += 1
            data.append(com_body[0])

print("Statistics")
print("Amount of posts = " + str(postcnt))
print("Amount of comments = " + str(commentcnt))

# extract to csv
df = pd.DataFrame(data)
df.to_csv("rddt.csv", index=False, header=False)
print("CSV conversion successful!")




# CURRENT PROBLEMS

# SOMEHOW FIGURE OUT HOW TO DEAL WITH STUFF LIKE "Delta" MISSING THE DICT HITS

# FULL COMPANY NAMES THAT ARE MORE THAN ONE WORD WILL NEVER GET HIT AS THE CURRENT ALGO CHECKS EACH WORD INDIVIDUALLY, SO MAYBE FIGURE OUT A BETTER WAY OF SEARCHING EACH STRING