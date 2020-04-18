API_KEY ='AIzaSyCIDOVFniO9R18E64-dMic6cvvgfdNy1Hk'
CLIENT_ID = '367580191273-38ujtdp9r7227kvge7b7md9k3mvai8g6.apps.googleusercontent.com'
SECRET = 'kgkQQbhIR4eqmE9xwgdMLk9d'

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from shared_db import setUpDatabase

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

#Average number of views for a "How To" Youtube Video
AVG_VIEWS = 8332

# Score is caluclated by dividing the video's views by the average views for 10 Youtube videos
# on a "How To" Youtube Video ("https://tubularinsights.com/average-youtube-views/"). 
#Then the amount of (likes/(likes + dislikes)) is added to the score (if applicable)
def calculate_score(views, likes, dislikes):
    score = views/(AVG_VIEWS * 10)
    if (likes + dislikes != 0):
        score += (likes / (likes + dislikes))
    return score

# Create a Youtube table if it doesn't exist already
def create_youtube_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Youtube (food TEXT PRIMARY KEY, score DOUBLE)")
    conn.commit()

# Insert values into Youtube table where results is a dictionary
# returned by the API
def insert_into_youtube(cur, conn, results):
    for food in results.keys():
        cur.execute("INSERT INTO Youtube (food, score) VALUES (?, ?)", (food, results[food]))
    conn.commit()

# Get list of foods to search for on Youtube
def gen_food_list(cur, conn):
    cur.execute('''SELECT DISTINCT cuisine FROM Cuisines''')
    country_list = cur.fetchall()
    food_list = []
    for country in country_list:
        cur.execute('''SELECT food FROM Cuisines WHERE cuisine = \"{}\"
        '''.format(country[0]))
        foods = cur.fetchall()
        cur.execute("SELECT food FROM Youtube")
        foods_in_data = cur.fetchall()
        #Duplicate check
        for food in foods:
            if (food not in foods_in_data):
                food_list.append(food[0])
                break
    conn.commit()
    return food_list

def get_results(food_list):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    results_dic = {}
    for food in food_list:
        request = youtube.search().list(
            part="snippet",
            maxResults=15,
            q="{} food".format(food)
        )
        try:
            res = request.execute()
        except:
            print("Connection error, returning progress")
            return results_dic
        video_ids = []
        #gets the video ids and stores them in video_ids
        for result in res['items']:
            if (result['id']['kind'] == 'youtube#video'):
                video_ids.append(result['id']['videoId'])
                if (len(video_ids) == 10):
                    break
        view_count = 0
        like_count = 0
        dislike_count = 0
        for vid in video_ids:
            request = youtube.videos().list(
                part='statistics',
                id=vid
            )
            try:
                res = request.execute()
            except:
                print("Connection error, returning progress")
                return results_dic
            view_count += int(res['items'][0]['statistics']['viewCount'])
            try:
                like_count += int(res['items'][0]['statistics']['likeCount'])
            except:
                pass
            try:
                dislike_count += int(res['items'][0]['statistics']['dislikeCount'])
            except:
                pass
        results_dic[food] = calculate_score(view_count, like_count, dislike_count)
    return results_dic

def main():
    cur, conn = setUpDatabase("stabiao.db")
    create_youtube_table(cur, conn)
    food_list = gen_food_list(cur, conn)
    results = get_results(food_list)
    insert_into_youtube(cur, conn, results)

    
if __name__ == "__main__":
    main()