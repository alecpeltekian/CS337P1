import re
import collections
import json
import sys
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import spacy
import statistics
from imdb import IMDb
from thefuzz import fuzz
import multiprocessing
import threading



# r"best.*drama"
# r"best.*(musical|comedy)"
# r"best.*(actress.*drama|drama.*actress)"
# r"best.*(actor.*drama|drama.*actor)"
# r"best.*(actress.*(comedy|musical)|(comedy|musical).*actress)"
# r"best.*(actor.*(comedy|musical)|(comedy|musical).*actor)"

stopWord = [
    "RT",
    "Golden Globes",
    "#GoldenGlobes",
    "golden globes",
    "golden",
    "globes",
    "Golden",
    "Globes",
    "GoldenGlobes",
    "#",
    "@goldenglobes",
    "best picture",
    "motion picture",
    "congratulations",
    "@huffpost",
    "drama",
]



json_file = sys.argv[1]

with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:   
        text = f.readline()
        dataset = json.loads(text)
print("done")

regex = r"best.*(musical|comedy)"

data = []
for i in range(len(dataset)):
    tweet = dataset[i]["text"]
    match = re.search(regex,tweet,re.IGNORECASE)
    if match:
        data.append(int(dataset[i]["timestamp_ms"]))

median = statistics.mode(data)

print(median)

releventTweets = []
for i in range(len(dataset)):
    time = int(dataset[i]["timestamp_ms"])
    if time < median-100000:
        continue
    if time > median+100000:
        break
    releventTweets.append(dataset[i]["text"])


res = {}
ia = IMDb()

def searchMovie(title,ia,res):
    movie = ia.search_movie(title)
    if not movie:
        return False
    movie = movie[0]
    if movie.has_key('year'):
            year = movie['year']
            if 2012 <= int(year) < 2013:
                if fuzz.token_sort_ratio(title,movie.get('title').lower()) > 85:
                    res[movie.get('title').lower()] = 1 + res.get(movie.get('title').lower(),0)

            
def extract_entities_pronouns(tweets,regex):
    sp = spacy.load("en_core_web_sm")
    people = {}
    nameList = []
    for tweet in tweets:
        if not re.search(regex,tweet,re.IGNORECASE):
            continue
        doc = sp(tweet)
        new = []
        for pos in doc:
            if (pos.pos_ in ["PROPN","NOUN","ADP"] and pos.text not in stopWord):
                new.append(pos.text)
            else:
                if new:
                    nameList.append((" ".join(new)).lower())
                    new = []
        #in case it ends in a movie name
        if new:
            nameList.append((" ".join(new)).lower())
    
    processes = []
    for i in range(0,len(nameList),100):
        print(i)
        for j in range(100):
            if i+j >= len(nameList):
                break
            name = nameList[i+j]
            p = threading.Thread(target = searchMovie,args=[name,ia,people])
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    return people




def wordPOS(sentence):
    sp = spacy.load("en_core_web_sm")
    res = {}
    doc = sp(sentence)
    for pos in doc:
        res[pos] = pos.pos_

    return res




print(len(releventTweets))    
print("compiling list")


sample = [
    "I just watched life of pi. It was aight",
    "I hope django unchained wins best pic"
]


res = extract_entities_pronouns(releventTweets,regex)
#print(wordPOS("I just watched life of pi. It was aight"))

print(res)
















