import re


nomineeListBestPicDrama = [
    "Argo",
    "Django Unchained",
    "Life of Pi",
    "Lincoln",
    "Zero Dark Thirty"
]


# Open the input file containing the tweets
with open('winnerTweets.txt', 'r') as input_file:
    tweets = input_file.readlines()

dictt = {}
for t in tweets:
    for n in nomineeListBestPicDrama:
        if re.search(n, t,re.IGNORECASE):
            dictt[n] = 1 + dictt.get(n,0)

print(dictt)