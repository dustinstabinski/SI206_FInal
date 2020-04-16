#! usr/bin/env python3
import praw
import pandas as pd
import datetime as dt

from shared_db import setUpDatabase

reddit = praw.Reddit(client_id='Tl2Em2AEss0rXA',
                        client_secret='r3hqoJ7-dELFLh9smnQyGFfkdSY',
                        user_agent='stabiao',
                        username='fotofronk',
                        password='Frankliao25')

#Calculate Reddit Score
def calculate_score(likes, comments):
    score = likes + (1.5 * comments)

    return score

# Create a Reddit table if it doesn't exist already
def create_reddit_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Reddit (food TEXT PRIMARY KEY, score DOUBLE)")
    conn.commit()

# Insert values into Reddit table where results is a dictionary
# returned by the API
def insert_into_reddit(cur, conn, results):
    for food in results.keys():
        cur.execute("INSERT INTO Reddit (food, score) VALUES (?, ?)", (food, results[food]))
    conn.commit()

# Get list of foods to search for on Reddit
def gen_food_list(cur, conn):
    cur.execute('''SELECT DISTINCT cuisine FROM Cuisines''')
    country_list = cur.fetchall()
    food_list = []
    for country in country_list:
        cur.execute('''SELECT food FROM Cuisines WHERE cuisine = \"{}\"
        '''.format(country[0]))
        foods = cur.fetchall()
        cur.execute("SELECT food FROM Reddit")
        foods_in_data = cur.fetchall()
        #Duplicate check
        for food in foods:
            if (food not in foods_in_data):
                food_list.append(food[0])
                break
    conn.commit()
    return food_list

def search_reddit(food_list):

    subreddit = reddit.subreddit('food')
    results_yt = {}
    like_count = 0
    comment_count = 0

    for food in food_list:
        like_count = 0
        comment_count = 0

        top_subreddit = subreddit.search(food ,limit = 10)

        topics_dict = { "score":[],
                    "comms_num": []}
        
        for submission in top_subreddit:
            topics_dict["score"].append(submission.score)
            topics_dict["comms_num"].append(submission.num_comments)

        for x in topics_dict["score"]:
            like_count = like_count + x

        for x in topics_dict["comms_num"]:
            comment_count = comment_count + x
        
        
        results_yt[food] = calculate_score(like_count, comment_count)
    return results_yt

def main():
    cur, conn = setUpDatabase("stabiao.db")
    create_reddit_table(cur, conn)
    food_list = gen_food_list(cur, conn)
    results = search_reddit(food_list)
    insert_into_reddit(cur, conn, results)

if __name__ == "__main__":
    main()