import re
import numpy as np
import spacy
from spacy import displacy

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
                    if (word.label_ == "PERSON" or word.text == "goldenglobes"):
                        count += 1
                for word in doc:
                    if (word.text in keywords):
                        keycount += 1
               # for token in doc:
                #    if (token.pos_ == "NOUN"):
                #        final = final + " " + token.text
                if (count == 0 and keycount > 0):
                    list.append(extracted)


    return unique_list(list)

def unique_list(list):
    out = []
    for word in list:
        if word not in out:
            out.append(word)
    return out

with open('TweetText.txt','r') as f:
    tweets = f.read().splitlines()

x = award_names(tweets)

with open('awardnames.txt', 'w') as output:
    for word in x:
        output.write('   ')
        output.write(word)
        output.write('\r')