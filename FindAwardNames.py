import re
import numpy as np
import spacy
from spacy import displacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

NER = spacy.load("en_core_web_sm")

def award_names(tweets):
    award_regex = r"((B|b)est(?=\s[A-Z])(?:\s([A-Z]\w+|in|a|by an|\s-\s))+)"  
    award_list = parse_tweets(tweets, award_regex)
    return award_list

with open("terminatingList.txt") as f:
    excluded = f.read().splitlines()

with open("keywords.txt") as f:
    keywords = f.read().splitlines()

def parse_tweets(tweets, regexp, list=[]):
    '''Take Tweet and seperate out id and text, search text for regexp, if match then add to dictionary'''
    for tweet in tweets:
        ##maybe add stop list before matching
        match =  re.search(regexp, tweet)
        if(match != None):
            extracted = match.group(0)
            extracted = re.split(" ", extracted)
            extracted = [x for x in extracted if x not in excluded]
            extracted = " ".join(extracted)
            extracted = extracted.lower()
            number = len(extracted.strip().split())
            if (number > 3 and number < 8):
             #   list.append(extracted)
                doc = NER(extracted)
                count = 0
                keycount = 0
                for word in doc.ents:
                    if (word.label_ == "PERSON" or word.text == "goldenglobes" or word.text == "golden"):
                        count += 1
                for word in doc:
                    if (word.text in keywords):
                        keycount += 1
                if (count == 0 and keycount > 0):
                    list.append(extracted)
    return unique_list(list)

def unique_list(list):
    out = []
    for word in list:
        if ((word not in out) and compare_to_list(out, word)):
            out.append(word)
    return out

def compare_to_list(list, word):
    ret = True
    for i in range(len(list)):
        if (fuzz.ratio(word, list[i]) > 80):
            ret = False
    return ret


with open('TweetText.txt','r') as f:
    tweets = f.read().splitlines()

x = award_names(tweets)

y = []

for i in range(len(x) - 1):
    if (fuzz.ratio(x[i], x[i+1]) < 60):
        y.append(x[i])


with open('awardnames.txt', 'w') as output:
    for i in range(len(y)):
        output.write('   ')
        output.write(y[i])
        output.write('\r')