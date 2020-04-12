from bs4 import BeautifulSoup
import requests
import json
import pprint
import re
from selenium import webdriver
import time


# scrape food list from site
def get_json_dict():
    try:
        req = requests.get("https://www.tasteatlas.com/tag/top100?orderby=location")
    except:
        print("Request failed")
        req = "FAIL"
    soup = BeautifulSoup(req.text, "html.parser")
    return soup.find("script", type="application/ld+json").text

def get_countries():
    base = 'https://www.tasteatlas.com/100-most-popular-foods-in-'
    f = open("countries" ,'r')
    num = 0
    # list of countries that were found in database
    countries = ['Argentina', 'Canada', 'China', 'Croatia', 'Czech-Republic', 'France', 'Germany', 'Greece', 'Hungary', 'India', 'Indonesia', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania', 'Spain', 'Sweden', 'Thailand', 'Turkey', 'United-Kingdom', 'USA', 'Vietnam']
    countries = ['Turkey', 'Vietnam', 'usa']
    food_dict = {}
    for c in countries:
        try:
            req = requests.get(base + c)
        except:
            print("Connection Error")
            break
        soup = BeautifulSoup(req.text, "html.parser")
        driver = webdriver.PhantomJS()
        driver.get(base+c)
        time.sleep(5)
        out = driver.execute_script('x = document.getElementsByClassName(\'h1 h1--bold\');var data = [];for (i = 0; i < x.length; i++) {data.push(x[i].innerHTML)}return data;')
        out = out[0:50]
        for index in range(len(out)):
            out[index] = out[index].replace('\n', '')
        food_dict[c] = out
    print(food_dict)
    f.close()
    
    
        

def main():
    f = open("food_data.json")
    d = json.load(f)


if __name__ == "__main__":
    main()
    