import json
import re
import sys


json_file = sys.argv[1]

with open(json_file, 'r') as f:   
        text = f.readline()
        data = json.loads(text)

def textSplit(dataset):
    with open('TweetText.txt', 'w') as output:
        for index in range(len(dataset)):
            for key in dataset[index]:
                if key == 'text':
                    text = dataset[index][key]
                    output.write('   ')
                    output.write(text)
                    output.write('\r')



print(textSplit(data))