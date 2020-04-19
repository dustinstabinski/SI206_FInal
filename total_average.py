from plot_youtube import get_food_genre_scores_y
from plot_reddit import get_food_genre_scores_r
from shared_db import setUpDatabase

def main():
    cur, conn = setUpDatabase("stabiao.db")
    youtube = get_food_genre_scores_y(cur, conn)
    reddit = get_food_genre_scores_r(cur, conn)
    total_dict = {}
    for country in youtube.keys():
        total_dict[country] = youtube[country] + reddit[country]
    f = open("Total_Results.txt", 'w')
    f.write("Average Reddit+Youtube score for each Country\n")
    for key in total_dict.keys():
        f.write(str(key) + ': ' + str(total_dict[key]) + '\n')
    f.close()

if __name__ == "__main__":
    main()