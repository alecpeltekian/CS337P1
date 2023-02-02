import re
import collections
import json
import sys
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import spacy
import statistics
from imdb import IMDb, IMDbError
from thefuzz import fuzz
import multiprocessing
import threading

dictAwardToRegex = {
    "best drama": r"best.*drama",
    "best musical/comedy": r"best.*(musical|comedy)",
    "best drama actor": r"best.*(actor.*drama|drama.*actor)",
    "best drama actress": r"best.*(actress.*drama|drama.*actress)",
    "best comedy/musical actress": r"best.*(actress.*(comedy|musical)|(comedy|musical).*actress)",
    "best comedy/musical actor": r"best.*(actor.*(comedy|musical)|(comedy|musical).*actor)",
    "best supporting actress": r"(best\s+)?support.*actress",
    "best supporting actor": r"(best\s+)?support.*actor",
    "best director": r"best\s+director",
    "best screenplay": r"best\s+screenplay",
    "best animated picture": r"(best\s+)?animated\s+picture",
    "best non-english picture": r"(best\s+)?non-english\s+picture",
    "best score": r"best\s+director",
    "best song": r"best\s+director",
    "best drama series": r"best\s+drama\s+series",
    "best musical/comedy series": r"best\s+(musical\/comedy|musical|comedy)",
    "best limited series": r"best\s+limited\s+series",
    "best limited series actress": r"best\s+limited\s+series\s+actress",
    "best limited series actor": r"best\s+limited\s+series\s+actor",
    "best television drama actress": r"best\s+television\s+drama\s+actress",
    "best television drama actor": r"best\s+television\s+drama\s+actor",
    "best television musical/comedy actor": r"best television (musical\/comedy|comedy\/musical|musical and comedy) actor",
    "best television musical/comedy actress": r"best television (musical\/comedy|comedy\/musical|musical and comedy) actress",
    "Cecil B. deMille": r"Cecil.*deMille|deMille.*Cecil"
}


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

print("going through tweets")

with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:   
        text = f.readline()
        dataset = json.loads(text)

print("done going through tweets")

ia = IMDb()

print("finding the announcement time for each award")

dictAwardMentionTimes = collections.defaultdict(list)
for tweet in dataset:
    for award,regex in dictAwardToRegex.items():
        if re.search(regex, tweet["text"]):
            dictAwardMentionTimes[award].append(tweet["timestamp_ms"])

dictAwardtoAnnoucetime = {}
for award, listOfTimes in dictAwardMentionTimes.items():
    announcementTime = statistics.mode(listOfTimes)
    dictAwardtoAnnoucetime[award] = announcementTime

print("finished all preprocessing")

def searchMovie(title,ia):
    try: 
        movie = ia.search_movie(title)
        if not movie:
            return 
        movie = movie[0]
        if movie.has_key('year'):
            year = movie['year']
            print(f"{title}: {year}")
            if 2012 <= int(year) <= 2013:
                if fuzz.token_sort_ratio(title,movie.get('title').lower()) > 85:
                    print("here")
                    res[movie.get('title').lower()] = 1 + res.get(movie.get('title').lower(),0)
    except Exception:
        print(f"{title} failed")


def extract_entities_pronouns(tweets,regex):
    sp = spacy.load("en_core_web_sm")
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
    
    print(f"searching through {len(nameList)} for possible nominees")

    processes = []
    for i in range(0,len(nameList),50):
        print(i)
        for j in range(50):
            if i+j >= len(nameList):
                break
            name = nameList[i+j]
            p = threading.Thread(target = searchMovie,args=[name,ia])
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    return res


def getNominees(award):
    if award not in dictAwardtoAnnoucetime:
        print(f"Please input an award from {dictAwardtoAnnoucetime.keys()}")
        return

    regex = dictAwardToRegex[award]

    releventTweets = []
    announcementTime = dictAwardtoAnnoucetime[award]
    for i in range(len(dataset)):
        time = int(dataset[i]["timestamp_ms"])
        if time < announcementTime-100000:
            continue
        if time > announcementTime+100000:
            break
        releventTweets.append(dataset[i]["text"])

    print(f"scanning through {len(releventTweets)} tweets for nominees \n")

    res = extract_entities_pronouns(releventTweets,regex)

    print(f"nominees are {res}")

def getBestMoment():
    sp = spacy.load("en_core_web_sm")
    releventTweets = []
    for tweet in dataset:
        if re.search(r'\bbest\w* moment\b', tweet["text"],re.IGNORECASE):
            releventTweets.append(tweet["text"])
    print(len(releventTweets))
    nameList = []
    for tweet in releventTweets:
        doc = sp(tweet)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text not in stopWord:
                if ent.text[-2:] == "'s":
                    nameList.append(ent.text[:-2])
                else:
                    nameList.append(ent.text)

    
    for name in nameList:
        res[name] = 1 + res.get(name,0)

    bestMomentPerson = [k for k, v in sorted(res.items(), key=lambda x: x[1])][-1]


    bestMomentTweets = []
    for tweet in releventTweets:
        if bestMomentPerson in tweet:
            bestMomentTweets.append(tweet)
    
    print(bestMomentTweets)

            




print("finding nominees for best pic")
res = {}
# getNominees("best drama")


#searchMovie('argo',ia)

getBestMoment()











