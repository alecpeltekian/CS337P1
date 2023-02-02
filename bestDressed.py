import re
import numpy as np
import spacy
from spacy import displacy
import heapq

NER = spacy.load("en_core_web_sm")

with open('TweetText.txt', 'r') as input_file:
    tweets = input_file.readlines()

def bestdressed_names(tweets):
    bdressed_regex = [r"(best dressed[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(best dress[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(best dressed is[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(best dressed goes to[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(best dressed =[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",]
    host_list = parse_tweets_best(tweets, bdressed_regex)
    return host_list

def worstdressed_names(tweets):
    wdressed_regex = [r"(worst dressed[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(worst dressed is[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(worst dressed goes to[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(worst dressed =[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
    r"(worstdressed[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(ugly dress?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)",
    r"(terrible dress?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"]
    
    host_list = parse_tweets_worst(tweets, wdressed_regex)
    return host_list

def parse_tweets_best(tweets, regexp, list=[]):
    '''Take Tweet and seperate out id and text, search text for regexp, if match then add to dictionary'''
    for reg in regexp:
        for tweet in tweets:
            tweet = re.sub(r'^.*?best', 'best', tweet)
            match =  re.search(reg, tweet)
            if(match != None):
                extracted = match.group(0)
                list.append(extracted)

    return list

def parse_tweets_worst(tweets, regexp, list=[]):
    '''Take Tweet and seperate out id and text, search text for regexp, if match then add to dictionary'''
    for reg in regexp:
        for tweet in tweets:
            tweet = re.sub(r'^.*?worst', 'worst', tweet)
            match =  re.search(reg, tweet)
            word = findWholeWord('worst dressed')(tweet)
            if(match != None):
                extracted = match.group(0)
                list.append(extracted)
            elif(word != None and len(list) < 10):
                list.append(tweet)
    return list

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def dressed_Voting(hostlist):
    names = []
    votes = []

    for i in hostlist:
        doc = NER(i)
        for word in doc.ents:
            if (word.label_ == "PERSON" and word.text != "GoldenGlobes"):
                if word.text in names:
                    votes[names.index(word.text)] += 1
                else:
                    names.append(word.text)
                    votes.append(1)
    return (names, votes)
y = worstdressed_names(tweets)
#print(y)
name2, vote2 = dressed_Voting(y)
ind = [vote2.index(y) for y in sorted(vote2, reverse=True)[:1]]
print("worst dressed")
print(name2[ind[0]])
x = bestdressed_names(tweets)
#print(x)
name, vote = dressed_Voting(x)
ind = [vote.index(x) for x in sorted(vote, reverse=True)[:1]]
print("best dressed")
print(name[ind[0]])


