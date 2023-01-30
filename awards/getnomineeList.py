import re

with open('TweetText.txt', 'r') as input_file:
    tweets = input_file.readlines()

def filter_tweets(regexp,related=True):
    listt = []
    for t in tweets:
        match =  re.search(regexp, t)
        if(related):
            if(match != None):
                listt.append(t)
        else:
            if(match == None):
                listt.append(t)
    return listt

def get_nominee_tweets():
    # find tweets relating to nomination
    regexp = re.compile('nomin((?:(?:at(?:ed|ion)))|ee)')
    nominee_tweets = filter_tweets(regexp)
    ##find tweets relating to winning?
    return nominee_tweets


l = get_nominee_tweets()
print(l)
print(len(l))