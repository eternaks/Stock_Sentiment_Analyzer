import asyncpraw
import asyncio
from praw.models import MoreComments
from dotenv import load_dotenv
import os
import data_preprocessing
import model_prediction

load_dotenv()

async def submission_stream(reddit):
    print("submission stream initialized")
    subreddit = await reddit.subreddit("wallstreetbets")
    cnt = 1

    async for submission in subreddit.stream.submissions(skip_existing=True):
        print("Post " + str(cnt) + " processed")
        cnt+=1

        # preprocess post title
        sub_title = data_preprocessing.clean_data(submission.title)
        sub_title = data_preprocessing.validate(sub_title)

        # preprocess post body
        sub_titletxt = data_preprocessing.clean_data(submission.selftext)
        sub_titletxt = data_preprocessing.validate(sub_titletxt)

        # predict and append to database
        if sub_title[1]:
            model_prediction.predict(sub_title[0], 0)

        # predict and append to database
        if sub_titletxt[1]:
            model_prediction.predict(sub_titletxt[0], 0)


async def comment_stream(reddit):
    print("comment stream initialized")
    subreddit = await reddit.subreddit("wallstreetbets")
    cnt = 1

    async for comment in subreddit.stream.comments(skip_existing=True):
        print("Comment " + str(cnt) + " processed")
        cnt+=1

        # fix weird bug with comment
        if isinstance(comment, MoreComments):
            continue

        # more data cleaning
        com_body = data_preprocessing.clean_data(comment.body)
        com_body = data_preprocessing.validate(com_body)

        # predict and append to database
        if com_body[1]:
            model_prediction.predict(com_body[0], 1)


async def main():
    reddit = asyncpraw.Reddit(
        client_id = os.getenv('client_id'),
        client_secret = os.getenv('client_secret'),
        user_agent = os.getenv('user_agent')
    )
    await asyncio.gather(
        comment_stream(reddit),
        submission_stream(reddit)
    )

if __name__ == "__main__":
    asyncio.run(main())