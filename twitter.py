from tweepy import OAuthHandler

# Inport all statements needed
import requests
import os
import json
import tweepy
import twitter_info #the keys
from pprint import pprint

# Handles Twitter Authentication and connection to the Twitter API
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth) #wtf does this do

#Average number of likes for a tweet
AVG_LIKES = 1690.46

# Score is calculated by dividing the tweet's likes by the average likes for 10 tweets
def calculate_score(likes):
    score = likes/(AVG_LIKES * 10)
    return score

# Create a Twitter table if it doesn't exist already
def create_twitter_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Twitter (food TEXT PRIMARY KEY, score DOUBLE)")
    conn.commit()

# Insert values into Twitter table where results is a dictionary
# returned by the API
def insert_into_twitter(cur, conn, results):
    for food in results.keys():
        cur.execute("INSERT INTO Twitter (food, score) VALUES (?, ?)", (food, results[food]))
    conn.commit()

# Get list of foods to search for on Twitter
def gen_food_list(cur, conn):
    cur.execute('''SELECT DISTINCT cuisine FROM Cuisines''')
    country_list = cur.fetchall()
    food_list = []
    for country in country_list:
        cur.execute('''SELECT food FROM Cuisines WHERE cuisine = \"{}\"
        '''.format(country[0]))
        foods = cur.fetchall()
        cur.execute("SELECT food FROM Twitter")
        foods_in_data = cur.fetchall()
        #Duplicate check
        for food in foods:
            if (food not in foods_in_data):
                food_list.append(food[0])
                break
    conn.commit()
    return food_list

def TwitterSearcher():
 """   
    max_tweets = 2
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break
"""



def main():
    cur, conn = setUpDatabase("stabiao.db")
    create_twitter_table(cur, conn)
    food_list = gen_food_list(cur, conn)
    results = get_results(food_list)
    insert_into_twitter(cur, conn, results)

    
if __name__ == "__main__":
    main()