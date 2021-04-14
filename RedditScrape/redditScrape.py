import os
import datetime
import csv
import pandas as pd
import praw
from psaw import PushshiftAPI
from Creds import *

# OAuth
reddit = praw.Reddit(client_id=PersonalUseScript, client_secret=Secret, user_agent=AppName)

api = PushshiftAPI(reddit)

# TODO Should define as a function to enable users to set date parameters

# set date
start_time = datetime.datetime(2021, 4, 3)
end_time = start_time + datetime.timedelta(days=1)


# pull data
submissions = list(api.search_submissions(after=int(start_time.timestamp()),
                                          before=int(end_time.timestamp()),
                                          subreddit='wallstreetbets'))

comments = list(api.search_comments(after=int(start_time.timestamp()),
                                    before=int(end_time.timestamp()),
                                    subreddit='wallstreetbets'))


# setup dataframe
submissions_df = pd.DataFrame(
    ([post.created_utc, post.id, post.num_comments, post.score, post.upvote_ratio, post.title, post.selftext, post.url] for post in submissions),
    columns=['CreatedUTC', 'SubmissionID', 'Num_Comments', 'VoteScore', 'UpVoteRatio', 'Title', 'Text', 'URL']
)

comments_df = pd.DataFrame(
    ([post.created_utc, post.submission, post.body, post.permalink] for post in comments),
    columns=['CreatedUTC', 'SubmissionID', 'Body', 'PermaLink'])


# Export CSV
os.makedirs("results", exist_ok=True)
submissions_df.to_csv(os.path.join("results", "submissions.csv"))
comments_df.to_csv(os.path.join("results", "comments.csv"))
