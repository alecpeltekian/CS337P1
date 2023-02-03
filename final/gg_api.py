import re
import collections
import json
import sys
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import spacy
from spacy import displacy
import statistics
from imdb import IMDb, IMDbError
from thefuzz import fuzz
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import multiprocessing
import threading
from nomineeHelper import *
from winnerHelper import *
from bestandworstdressHelper import *
from hostsHelper import *


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

print("finding the announcement time for each award")

dictAwardMentionTimes = collections.defaultdict(list)
for tweet in dataset:
    for award,regex in dictAwardToRegex.items():
        if re.search(regex, tweet["text"]):
            dictAwardMentionTimes[award].append(tweet["timestamp_ms"])

dictAwardtoAnnoucetime = {}
for award, listOfTimes in dictAwardMentionTimes.items():
    announcementTime = statistics.median(listOfTimes)
    dictAwardtoAnnoucetime[award] = announcementTime


print("importing different lists into frame")

with open("terminatingList.txt") as f:
    excludeList = f.read().splitlines()

with open("regexListWinners.txt") as f:
    regexWinnerList = f.read().splitlines()

with open('TweetText.txt', 'w', errors='ignore') as output:
    for index in range(len(dataset)):
        output.write(dataset[index]["text"])
        output.write('\n')

with open('TweetText.txt', 'r', errors='ignore') as input_file:
    tweets = input_file.readlines()

print("finished all preprocessing")

















#awardname -> listofNominees
def getNominees(award):
    res = {}
    ia = IMDb()
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

    res = extract_entities_pronouns(releventTweets,regex,res,ia)

    #res = [k for k, v in sorted(res.items(), key=lambda x: x[1])][-1]

    return ("NOMINEES:",res.keys())

#None -> listOfBestMoment
def getBestMoment():
    sp = spacy.load("en_core_web_sm")
    releventTweets = []
    for tweet in dataset:
        if re.search(r'\bbest\w* moment\b', tweet["text"],re.IGNORECASE):
            releventTweets.append(tweet["text"])
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
    
    return bestMomentTweets

#listofNominees->winner
def getWinners(nomineeList, entity):
    winnerTweets = []
    for tweet in dataset:
        for regex in regexWinnerList:
            match = re.search(regex, tweet["text"])
            if match:
                winnerTweets.append(tweet["text"])
                break
    nomineeDict = {}
    for nom in nomineeList:
        nomineeDict[nom] = nameToRegex(nom,entity)
    dictt = {}
    for tweet in winnerTweets:
        for nominee, regex in nomineeDict.items():
            if re.search(regex,tweet):
                dictt[nominee] = 1 + dictt.get(nominee,0)
    return ("Winner",max(dictt, key=dictt.get))

#none ->best and worst dressed
def getBestandWorstDressed():
    y = worstdressed_names(tweets)
    #print(y)
    name2, vote2 = dressed_Voting(y)
    ind = [vote2.index(y) for y in sorted(vote2, reverse=True)[:1]]
    x = bestdressed_names(tweets)
    #print(x)
    name, vote = dressed_Voting(x)
    ind = [vote.index(x) for x in sorted(vote, reverse=True)[:1]]
    return ("WORST DRESSED", name2[ind[0]], "BEST DRESSED", name[ind[0]])

#none -> hosts
def getHosts():
    x = host_names(tweets)
    name, vote = HostVoting(x)
    ind = [vote.index(x) for x in sorted(vote, reverse=True)[:2]]
    return (name[ind[0]], name[ind[1]])


#print(getNominees("best drama"))
print(getBestandWorstDressed())
#print(getNominees("best drama series"))

# nom1 = ["Anne Hathaway", "Amy Adams", "Helen Hunt", "Nicole Kidman"]
# nom2 = ["Christopher Waltz","Alan Arkin","Leonardo DiCaprio","Tommy Lee Jones","Phillip Seymour Hoffman"]
# nom3 = ["Brave","Frankenweenie","Hotel Transylvania","Rise of the Guardians","Wreck-It Ralph"]
# nom4 = ["Homeland","Breaking Bad","Boardwalk Empire","Downton Abbey","The Newsroom"]
# print(getWinners(nom1,"person"))
# print(getWinners(nom2,"person"))
# print(getWinners(nom3,"movie"))
# print(getWinners(nom4,"movie"))


# print("BEST MOMENT", getBestMoment())

# print("HOST", getHosts())

# print(getBestandWorstDressed())









