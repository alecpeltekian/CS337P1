import re
import numpy as np
import spacy
from spacy import displacy
import heapq

NER = spacy.load("en_core_web_sm")

with open('TweetText.txt', 'r') as input_file:
    tweets = input_file.readlines()

def host_names(tweets):
    host_regex = [r"(host[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", 
     r"(host[s]?[:]?\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+))[\s]+(and|&)[\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+))"]
    host_list = parse_tweets(tweets, host_regex)
    return host_list

def parse_tweets(tweets, regexp, list=[]):
    '''Take Tweet and seperate out id and text, search text for regexp, if match then add to dictionary'''
    for reg in regexp:
        for tweet in tweets:
            match =  re.search(reg, tweet)
            if(match != None):
                extracted = match.group(0)
                list.append(extracted)
    return list

def HostVoting(hostlist):
    names = []
    votes = []

    for i in hostlist:
        doc = NER(i)
        for word in doc.ents:
            if (word.label_ == "PERSON"):
                if word.text in names:
                    votes[names.index(word.text)] += 1
                else:
                    names.append(word.text)
                    votes.append(1)
    return (names, votes)

x = host_names(tweets)
name, vote = HostVoting(x)
ind = [vote.index(x) for x in sorted(vote, reverse=True)[:2]]
print(name[ind[0]], name[ind[1]])
with open('hostnames.txt', 'w') as output:
    output.write('   ')
    output.write(name[ind[0]])
    output.write('\r')
    output.write('   ')
    output.write(name[ind[1]])
    output.write('\r')