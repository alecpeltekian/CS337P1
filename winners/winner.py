import re
import sys


#just produces a text of tweets where each tweet might tell us that someone/something won an award 


tweetTxt = sys.argv[1]

# Open the input file containing the tweets
with open(tweetTxt, 'r') as input_file:
    tweets = input_file.readlines()

with open('regexList.txt','r') as f:
    regex_list = f.read().splitlines()

# Open the output file to write the matching tweets
with open('winnerTweets.txt', 'w') as output_file:
    for tweet in tweets:
        for regex in regex_list:
            match = re.search(regex, tweet)
            if match:
                output_file.write(tweet)
                break