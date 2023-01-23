import json
import re
import sys


json_file = sys.argv[1]

with open(json_file, 'r') as f:   
        text = f.readline()
        data = json.loads(text)

def textSplit(dataset):
    for index in range(len(dataset)):
        for key in dataset[index]:
            if key == 'text':
                text = dataset[index][key]
                print(text,"\n")

print(textSplit(data))