import praw
from praw.models import MoreComments
from dotenv import load_dotenv
import os
import data_preprocessing
import model_prediction

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('client_id'),
    client_secret = os.getenv('client_secret'),
    user_agent = os.getenv('user_agent')
)


subreddit = "wallstreetbets"

def submission_stream():
    print("submission stream successful")
    for submission in reddit.subreddit(subreddit).stream.submissions(skip_existing=True):

        # preprocess post title
        sub_title = data_preprocessing.clean_data(submission.title)
        sub_title = data_preprocessing.validate(sub_title)

        # preprocess post body
        sub_titletxt = data_preprocessing.clean_data(submission.selftext)
        sub_titletxt = data_preprocessing.validate(sub_titletxt)

        # predict and append to database
        if sub_title[1]:
            model_prediction.predict(sub_title[0])

        # predict and append to database
        if sub_titletxt[1]:
            model_prediction.predict(sub_titletxt[0])

def comment_stream():
    print("comment stream successful")
    for comment in reddit.subreddit(subreddit).stream.comments(skip_existing=True):
        # more data cleaning
        com_body = data_preprocessing.clean_data(comment)
        com_body = data_preprocessing.validate(com_body)

        # predict and append to database
        if com_body[1]:
            model_prediction.predict(com_body[0])