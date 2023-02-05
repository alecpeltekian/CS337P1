import spacy
import re
from thefuzz import fuzz
import threading
import requests
from collections import Counter

res = {}


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
    "amp",
    "pantsuit",
    "luv u",
    "caraca",
    "flu",
    "oscars",
    "Oscar"
    "Amy Poehler",
    "Tina Fey",

]

with open('males.txt', 'r') as input_file:
    males = input_file.read().splitlines()



with open('females.txt', 'r') as input_file:
    females = input_file.read().splitlines()

def searchMovie(title,res):
    request = f"https://www.omdbapi.com/?apikey=54039ca8&t={title}"
    response = requests.get(request)
    if response.status_code != 200:
        return
    data = response.json()

    if data['Response'] == "False":
        return
    year = data['Year'][:4]
    if 2007 <= int(year) <= 2013:
        if fuzz.token_sort_ratio(title,data['Title'].lower()) > 85 and data['Title'].lower() not in stopWord:
            res[data['Title'].lower()] = 1 + res.get(data['Title'].lower(),0)

def extract_people(tweets,gender):
    sp = spacy.load("en_core_web_sm")
    nameList = []
    for tweet in tweets:
        doc = sp(tweet)
        for ent in doc.ents:
            if ent.label_== "PERSON" and ent.text not in stopWord:
                firstName = ent.text.split(" ")[0] if " " in ent.text else ent.text
                if gender == 2 and firstName not in males:
                    continue
                if gender == 3 and firstName not in females:
                    continue
                nameList.append(ent.text)
    counter = Counter(nameList)
    return counter


def extract_entities_pronouns(tweets,res):
    sp = spacy.load("en_core_web_sm")
    nameList = []
    for tweet in tweets:
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
    
    
    if len(nameList) > 3000:
        nameList = nameList[(len(nameList)//2)-1500:(len(nameList)//2)+1500]

    #print(f"searching through {len(nameList)} for possible nominees")
    processes = []
    for i in range(0,len(nameList),200):
      
        for j in range(1,200,2):
            if i+j >= len(nameList):
                break
            name = nameList[i+j]
            p = threading.Thread(target = searchMovie,args=[name,res])
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    return res