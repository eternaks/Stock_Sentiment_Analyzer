import praw
import private_vars
from praw.models import MoreComments
import pandas as pd

def remove_newline(var1):
    var1 = var1.replace("\n\n", ". ")
    var1 = var1.replace("\n", ". ")
    return var1

reddit = praw.Reddit(
    client_id = private_vars.client_id,
    client_secret = private_vars.client_secret,
    user_agent = private_vars.user_agent
)

postcnt = 0
commentcnt = 0

data = []

for submission in reddit.subreddit("wallstreetbets").new(limit=5):
    print(submission.title)
    sub_titletxt = submission.selftext

    # add title to dataset
    if sub_titletxt == "":
        data.append(remove_newline(submission.title))
        # print(data[len(data)-1])

    # add title body to dataset
    else:
        data.append(remove_newline(sub_titletxt))
        # print(data[len(data)-1])
    
    postcnt += 1
    firstcmt = True
    
    # process comments
    for top_level_comment in submission.comments:
        # ignore bot comment
        if (firstcmt):
            firstcmt = False
            continue

        # prevent weird bug with api
        if isinstance(top_level_comment, MoreComments):
            continue

        commentcnt += 1
        data.append(remove_newline(top_level_comment.body))
        # print(comment)

print("Statistics")
print("Amount of posts = " + str(postcnt))
print("Amount of comments = " + str(commentcnt))

# extract to csv
df = pd.DataFrame(data)
df.to_csv("test.csv", index=False, header=False)
print("CSV conversion successful!")


