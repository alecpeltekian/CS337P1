import re
import numpy as np
import spacy
from spacy import displacy
import heapq

NER = spacy.load("en_core_web_sm")

with open('TweetText.txt', 'r') as input_file:
    tweets = input_file.readlines()



def parse_tweets(tweets, list=[]):
    '''Take Tweet and seperate out id and text, search text for regexp, if match then add to dictionary'''
    
    for tweet in tweets:
        list.append(tweet)
    return list

def Voting(hostlist):
    names = []
    votes = []
    ind = 0

    for i in hostlist:
        if (ind < 100000):
            doc = NER(i)
            ind += 1
            for word in doc.ents:
                if (word.label_ == "PERSON" and word.text != "GoldenGlobes"):
                    if word.text in names:
                        votes[names.index(word.text)] += 1
                    else:
                        names.append(word.text)
                        votes.append(1)
    return (names, votes)

x = parse_tweets(tweets, [])
print("parsed")
name, vote = Voting(x)
print("voted")
ind = [vote.index(x) for x in sorted(vote, reverse=True)[:1]]
print(name[ind[0]])
