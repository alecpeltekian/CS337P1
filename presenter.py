import re

def get_presenters(tweets):
    presenters = []
    for tweet in tweets:
        words = tweet.split()
        for i, word in enumerate(words):
            if word.lower() in ["present", "presented", "speak", "spoke", "gave"]:
                if i > 0:
                    presenter = words[i-1]
                    if presenter[0].isupper():
                        presenters.append(presenter)
    return presenters

tweets = open("winnerTweets.txt", "r", errors='ignore')

print(get_presenters(tweets))