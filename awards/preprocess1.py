import json
import re
import sys


json_file = sys.argv[1]

with open(json_file, 'r', encoding='utf-8', errors='ignore') as f:   
        text = f.readline()
        data = json.loads(text)
print("done")

def jsonSplit(dataset):
    with open('TweetsTimes.json', 'w') as f:
        for i in range(len(dataset)):
            text = dataset[i]["text"]
            time = dataset[i]["timestamp_ms"]
            obj = [i,text,time]
            json.dump(obj, f)
            f.write('\n')
jsonSplit(data)
print("and done")
