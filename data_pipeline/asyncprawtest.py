import praw
import asyncpraw
import asyncio
from praw.models import MoreComments
import prawcore
from dotenv import load_dotenv
import os
# import data_preprocessing
# import model_prediction

load_dotenv()

async def comment_stream(reddit):
    print("comment stream successful")
    subreddit = await reddit.subreddit("wallstreetbets")
    async for comment in subreddit.stream.comments(skip_existing=True):
        print("comment")


async def submission_stream(reddit):
    print("submission stream successful")
    subreddit = await reddit.subreddit("wallstreetbets")
    async for submission in subreddit.stream.submissions(skip_existing=True):
        # do stuff
        print("submission")

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