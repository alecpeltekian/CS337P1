import re
import collections
with open("terminatingList.txt") as f:
        excludeList = f.read().splitlines()

def nameToRegex(name: str, entity) -> list:
    names = re.split(" ", name)
    if entity == "person":
        return f"(?i).*({'|'.join(names)}).*"
    elif entity == "movie":
        names = [x for x in names if x not in excludeList]
        names = "(?i)(?=.*" + ")(?=.*".join(names) + ").*"
        return names
    else:
        print(f"{entity} is Not A movie or Person!!")
    
# Open the input file containing the tweets
with open('winnerTweets.txt', 'r') as input_file:
    tweets = input_file.readlines()









#outputs best motion pic-drama
BestPicDrama = [
    "Argo",
    "Django Unchained",
    "Life of Pi",
    "Lincoln",
    "Zero Dark Thirty"
]

#outputs best motion pic-musical
BestPicMusic = [
    "Les Miserables",
    "The Best Exotic Marigold Hotel",
    "Moonrise Kingdom",
    "Salmon Fishing in the Yemen",
    "Silver Lining Playbook"
]

BestActressDrama = [
    'Jessica Chastain',
    'Marion Cotillard',
    'Helen Mirren',
    'Naomi Watts',
    'Rachel Weisz'
]


def getWinner(nomineeList, entity):
    nomineeDict = {}
    for nom in nomineeList:
        nomineeDict[nom] = nameToRegex(nom,entity)
    dictt = {}
    for t in tweets:
        for nominee, regex in nomineeDict.items():
            if re.search(regex,t):
                dictt[nominee] = 1 + dictt.get(nominee,0)
    print(max(dictt, key=dictt.get))

getWinner(BestPicDrama,"movie")
getWinner(BestPicMusic,"movie")
getWinner(BestActressDrama,"person")
