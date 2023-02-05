import re
import collections
import json
import sys
import spacy
from thefuzz import fuzz
from fuzzywuzzy import fuzz
from nomineeHelper import *
from winnerHelper import *
from bestandworstdressHelper import *
from hostsHelper import *
from presenterHelper import *
from awardHelper import *

MOVIE = 1
MALE = 2
FEMALE = 3
BOTH = 4


dictAwardToRegex = {
    "best drama": [r"best\s+motion\s+picture\s+drama",1],
    "best musical/comedy": [r"best.*(musical|comedy)",1],
    "best drama actor": [r"best\s+drama\s+actor",2],
    "best drama actress": [r"best\s+actress",3],
    "best comedy/musical actress": [r"best\s+actress\s+(musical|comedy)",3],
    "best comedy/musical actor": [r"best\s+actor+(musical|comedy)",2],
    "best supporting actress": [r"best\s+supporting\s+actress",3],
    "best supporting actor": [r"best\s+supporting\s+actor",2],
    "best director": [r"best\s+director",4],
    "best screenplay": [r"best\s+screenplay",4],
    "best animated picture": [r"best\s+animated\s+picture",1],
    "best non-english picture": [r"best\s+non-english\s+picture",1],
    "best score": [r"best\s+director",4],
    "best song": [r"best\s+song",1],
    "best drama series": [r"best\s+drama\s+series",1],
    "best musical/comedy series": [r"best\s+comedy\s+series",1],
    "best limited series": [r"best\s+limited\s+series",1],
    "best limited series actress": [r"best\s+limited\s+series",3],
    "best limited series actor": [r"best\s+limited\s+series",2],
    "best television drama actress": [r"best\s+television\s+drama",3],
    "best television drama actor": [r"best\s+television\s+drama",2],
    "best television musical/comedy actor": [r"best\s+television\s+comedy",2],
    "best television musical/comedy actress": [r"best\s+television\s+comedy",3],
    "Cecil B. deMille": [r"Cecil.*deMille|deMille.*Cecil",4],
    "best supporting TV actress": [r"best\s+supporting\s+tv",3],
    "best supporting TV actor": [r"best\s+supporting\s+tv",2]
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

print("doing some preprocessing")

dictAwardtoTweets = collections.defaultdict(list)
for award,lst in dictAwardToRegex.items():
    regex = lst[0]
    i = 0
    while i < len(dataset):
        if re.search(regex,dataset[i]["text"]):
            for j in range(max(0,i-200),min(i+200,len(dataset))):
            #for tweet in dataset[max(i-200,0):min(i+200,len(dataset))]:
                dictAwardtoTweets[award].append(dataset[j]["text"])
            i+=400
        else:
            i+=1


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
    if award not in dictAwardtoTweets:
        return None

    regex,entity = dictAwardToRegex[award]


    releventTweets = dictAwardtoTweets[award]
    if len(releventTweets) > 700:
        releventTweets = releventTweets[(len(releventTweets)//2)-350:(len(releventTweets)//2)+350]

    if entity == MOVIE:
        res = extract_entities_pronouns(releventTweets,res)
    else:
        res = extract_people(releventTweets,entity)
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)

    result = []
    for key,val in res:
        result.append(key)

    return result[:5]

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
def getWinners(nomineeList):
    entity = isPersonMovie(nomineeList)
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
            if re.search(regex,tweet,re.IGNORECASE):
                dictt[nominee] = 1 + dictt.get(nominee,0)
    return max(dictt, key=dictt.get)

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

def getAwards():

    x = award_names(tweets)

    y = []

    for i in range(len(x) - 1):
        if (fuzz.ratio(x[i], x[i+1]) < 60):
            y.append(x[i])

    return y

def getPresenters(award):
    lst = extractPresenter(award)
    x = extractFinal(lst)
    return x


def main():
    hosts = getHosts()
    print(f"Host: {hosts}")
    award_list = getAwards()
    print(f"Awards: {award_list}")
    jsonDict = {}
    jsonDict["Host"] = hosts

    for award in dictAwardToRegex.keys():
        print("\n")
        jsonDict[award] = {}
        print(f"Award: {award}")
        Nominee_List = getNominees(award)
        Presenter_List = getPresenters(award)
        if not Nominee_List:
            print(f"Presenters: {Presenter_List}")
            jsonDict[award]["Presenter"] = Presenter_List
            print(f"No more information for {award}")
            continue

        Presenter_List = getPresenters(award)
        winner = getWinners(Nominee_List)
        print(f"Presenters: {Presenter_List}")
        print(f"Nominees: {Nominee_List}")
        print(f"Winner: {winner}")
        jsonDict[award]["Presenter"] = Presenter_List
        jsonDict[award]["Nominees"] = Nominee_List
        jsonDict[award]["Winner"] = winner

    print(getBestMoment())
    print(getBestandWorstDressed())
        
    jsonFinal = json.dumps(jsonDict)
    print(jsonFinal)

main()

        
    











