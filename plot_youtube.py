import matplotlib
import matplotlib.pyplot as plt
import json
import os
import sqlite3
from shared_db import setUpDatabase

matplotlib.use('TkAgg')

# get the average of each cuisines score
def average(scores):
    total = 0
    for score in scores:
        total += score[0]
    return total / len(scores)

def get_food_genre_scores(cur, conn):
    cur.execute('''SELECT DISTINCT cuisine FROM Cuisines''')
    country_list = cur.fetchall()
    scores_dic = {}
    for country in country_list:
        cur.execute('''SELECT score FROM Youtube INNER JOIN 
        Cuisines ON Youtube.food = Cuisines.food WHERE cuisine = \"{}\"
        '''.format(country[0]))
        scores = cur.fetchall()
        if country not in scores_dic:
            scores_dic[country[0]] = average(scores)
        else:
            print("Error duplicate found")
            exit(1)
    # Write data to a file
    f = open("Youtube_Results.txt", 'w')
    f.write("Average Youtube score for each Country\n")
    for key in scores_dic.keys():
        f.write(str(key) + ': ' + str(scores_dic[key]) + '\n')
    f.close()
    return scores_dic

def plot(data):
    x_axis = list(data.keys())
    x_axis = sorted(x_axis)
    y_axis = []
    for country in x_axis:
        y_axis.append(data[country])
    colors = ["black", "grey", "lightcoral", "darkred", "red",
    "coral", "burlywood", "olive", "yellow", "forestgreen", 
    "aquamarine", "cadetblue", "navy", "slateblue", "darkorchid", 
    "violet", "purple", "aqua", "dodgerblue", "indigo"]
    plt.barh(x_axis, y_axis, color=colors, align="center")
    plt.xlabel('Average Score', fontsize=15)
    #plt.ylabel('Cuisine', fontsize=15)
    #plt.xticks(range(len(x_axis)), x_axis, fontsize=10, rotation=75)
    plt.title('Average Youtube Popularity Score for Cuisines around the World')
    for index, value in enumerate(y_axis):
        plt.text(value, index, str(round(value, 1)))
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    plt.show()
 

def main():
    cur, conn = setUpDatabase('stabiao.db')
    data = get_food_genre_scores(cur, conn)
    plot(data)


if __name__ == "__main__":
    main()