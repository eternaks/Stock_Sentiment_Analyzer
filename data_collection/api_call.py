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

def main():
    print("Beginning Scraping")

    # loop through most recent submissions in hot category
    for submission in reddit.subreddit("wallstreetbets").hot(limit=None):

        # Process submission body text
        sub_titletxt = data_preprocessing.clean_data(submission.selftext)
        sub_titletxt = data_preprocessing.validate(sub_titletxt)

        # Add to dataset if contains mention of stock ticker
        if sub_titletxt[1]:
            data.append(sub_titletxt[0])
            postcnt += 1

        # Process submission title text
        sub_title = data_preprocessing.clean_data(submission.title)
        sub_title = data_preprocessing.validate(sub_title)

        # Add to dataset if contains mention of stock ticker
        if sub_title[1]:
            data.append(sub_title[0])
            postcnt += 1

        # process post comments
        firstcmt = True
        for top_level_comment in submission.comments:
            # ignore bot comment
            if firstcmt:
                firstcmt = False
                continue
            
            # prevent weird bug with api, refer to praw documentation for more details
            if isinstance(top_level_comment, MoreComments):
                continue

            # process comment text
            com_body = data_preprocessing.clean_data(top_level_comment.body)
            com_body = data_preprocessing.validate(com_body)

            # add to dataset if contains mention of stock ticker
            if com_body[1]:
                commentcnt += 1
                data.append(com_body[0])

    # print how many total posts and comments were processed
    print("Statistics")
    print("Amount of posts = " + str(postcnt))
    print("Amount of comments = " + str(commentcnt))

    # extract to csv
    df = pd.DataFrame(data)
    df.to_csv("rddt.csv", index=False, header=False)
    print("CSV conversion successful!")

if __name__ == "__main__":
    main()