#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit(client_id='Tl2Em2AEss0rXA', \
                        client_secret='r3hqoJ7-dELFLh9smnQyGFfkdSY', \
                        user_agent='stabiao', \
                        username='fotofronk', \
                        password='Frankliao25')

def search_reddit():

    subreddit = reddit.subreddit('food')

    top_subreddit = subreddit.search(SEARCH_KEYWORD,limit = 5)

    topics_dict = { "title":[], \
                "score":[], \
                "id":[], "url":[], \ 
                "comms_num": [], \
                "created": [], \
                "body":[]}
    
    for submission in top_subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)