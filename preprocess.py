import json
import re
import sys


json_file = sys.argv[1]

with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:   
        text = f.readline()
        data = json.loads(text)
print("done")
def textSplit(dataset):
    with open('TweetTextTime.txt', 'w', errors='ignore') as output:
        for index in range(len(dataset)):
            for key in dataset[index]:
                if key == 'text':
                    text = dataset[index][key]
                    time = dataset[index]["timestamp_ms"]
                    text = f"{text}: {time}"
                    output.write('   ')
                    output.write(text)
                    output.write('\r')



print(textSplit(data))