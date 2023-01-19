import json

f = open('gg2013.json')
data = json.load(f)

import re
def textSplit(dataset):
    for index in range(len(dataset)):
        for key in dataset[index]:
            if key == 'text':
                text = dataset[index][key]
                print(text,"\n")

print(textSplit(data))