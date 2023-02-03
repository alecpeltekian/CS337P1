import re
import collections
import json
import sys
import numpy as np
# from scipy.stats import norm
# import matplotlib.pyplot as plt
import spacy
# import statistics
# from imdb import IMDb, IMDbError
# from thefuzz import fuzz
# import multiprocessing
# import threading


import re
with open('TweetText.txt', 'r') as input_file:
    tweets = input_file.readlines()
def filter_tweets(regexp,related=True):
    tweetlist = []
    for t in tweets:
        match =  re.search(regexp, t)
        if(related):
            if(match != None and 'RT' not in t):
                tweetlist.append(t)
        else:
            if(match == None):
                tweetlist.append(t)
    return tweetlist

def get_presenter_tweets():
    # find tweets relating to presenting
    regexp = re.compile('.+(are )?present(er|ed|ing|s|\s).+')
    present_tweets = filter_tweets(regexp)
    return present_tweets

presTweets = get_presenter_tweets()

import spacy
def extractPerson(sentences):
    nlp = spacy.load("en_core_web_sm")
    person_text = []
    for sentence in sentences:
        full = nlp(sentence)
        for pos in full.ents:
            if pos.label_ == "PERSON":
                person_text.append(sentence)
                break
    return person_text


people = extractPerson(presTweets)
print(people)
# print(len(people))


# def count_names(names):
#     name_counts = {}
#     filtered_names = []
#     for name in names:
#         name_text = name.text
#         if name_text.startswith("RT "):
#             continue
#         filtered_names.append(name_text)
#         if name_text in name_counts:
#             name_counts[name_text] += 1
#         else:
#             name_counts[name_text] = 1
#     return name_counts, filtered_names



# print(count_names(people))
"""
pseudocode

for every tweet in tweet list:
    replace punctuation with empty string, make it all lower case (normalize)

potential_pres_tweets = []
for every lower case tweet with no punctuation:
    if regex match for present(er|ing|s|\s):
        add to potential pres tweet list

for award in award_names:
    get shortened version, store in list called shortened_awards

for tweet in potential presenter tweets:
    find index of keyword "Best"
    award_name = ""
    from index to end of list:
         if the word is in the shortened awards list and the word is not motion or picture:
            add to award name with a space
    for award in shortened awards:
        find fuzz similarity
        find award name with maximum similarity
"""