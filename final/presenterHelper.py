import re
import spacy

dictAwardToRegex = {
    "best drama": r"best.*drama",
    "best musical/comedy": r"best.*(musical|comedy)",
    "best drama actor": r"best.*(actor.*drama|drama.*actor)",
    "best drama actress": r"best.*(actress.*drama|drama.*actress)",
    "best comedy/musical actress": r"best.*(actress.*(comedy|musical)|(comedy|musical).*actress)",
    "best comedy/musical actor": r"best.*(actor.*(comedy|musical)|(comedy|musical).*actor)",
    "best supporting actress": r"(best\s+)?support.*actress",
    "best supporting actor": r"(best\s+)?support.*actor",
    "best director": r"best\s+director",
    "best screenplay": r"best\s+screenplay",
    "best animated picture": r"(best\s+)?animated\s+picture",
    "best non-english picture": r"(best\s+)?non-english\s+picture",
    "best score": r"best\s+director",
    "best song": r"best\s+director",
    "best drama series": r"best\s+drama\s+series",
    "best musical/comedy series": r"best\s+(musical\/comedy|musical|comedy)",
    "best limited series": r"best\s+limited\s+series",
    "best limited series actress": r"best\s+limited\s+series\s+actress",
    "best limited series actor": r"best\s+limited\s+series\s+actor",
    "best television drama actress": r"best\s+television\s+drama\s+actress",
    "best television drama actor": r"best\s+television\s+drama\s+actor",
    "best television musical/comedy actor": r"best television (musical\/comedy|comedy\/musical|musical and comedy) actor",
    "best television musical/comedy actress": r"best television (musical\/comedy|comedy\/musical|musical and comedy) actress",
    "Cecil B. deMille": r"Cecil.*deMille|deMille.*Cecil"
}

import re
with open('TweetText.txt', 'r', errors='ignore') as input_file:
    tweets = input_file.readlines()
def filter_tweets(regexp,related=True):
    tweetlist = []
    for t in tweets:
        match =  re.search(regexp, t)
        if(related):
            if(match != None and 'RT' not in t):
                tweetlist.append(t)
        else:
            if(match == None):
                tweetlist.append(t)
    return tweetlist

def get_presenter_tweets():
    regexp = re.compile('.+(are )?present(er|ed|ing|s|\s).+')
    present_tweets = filter_tweets(regexp)
    return present_tweets

presTweets = get_presenter_tweets()

import spacy
def extractPerson(sentences):
    nlp = spacy.load("en_core_web_sm")
    person_text = []
    for sentence in sentences:
        full = nlp(sentence)
        for pos in full.ents:
            if pos.label_ == "PERSON":
                person_text.append(sentence)
                break
    return person_text


people = extractPerson(presTweets)

# print(len(people))

def extractPresenter(award):
    newlist = []
    for index in people:
        newlist.append((index.lower()))
        presenters = []
        for i in newlist:
            if re.findall(dictAwardToRegex[award], i):
                presenters.append(i)

    return presenters

listfinal = extractPresenter("best screenplay")

import spacy

def extractFinal(list):
    nlp = spacy.load("en_core_web_sm")
    finalPeople = []
    for i in list:
        if "present" in i:
            cut1 = i.split("present")[0]
            doc = nlp(cut1)
            for ent in doc.ents:
                if ent.label_== "PERSON":
                    finalPeople.append(ent.text)

    return finalPeople

def gettingPresenter(award):
    regex,entity = dictAwardToRegex[award]
    releventTweets = []
    for tweet in tweets:
        if re.search(regex,tweet["text"]):
            releventTweets.append(tweet["text"])
    presentingTweets = []
    for tweet in releventTweets:
        if re.search(r'\b(present|ed|ing)\b',tweet):
            presentingTweets.append(tweet)
    print(presentingTweets)





# def count_names(names):
#     name_counts = {}
#     filtered_names = []
#     for name in names:
#         name_text = name.text
#         if name_text.startswith("RT "):
#             continue
#         filtered_names.append(name_text)
#         if name_text in name_counts:
#             name_counts[name_text] += 1
#         else:
#             name_counts[name_text] = 1
#     return name_counts, filtered_names



# print(count_names(people))


"""
pseudocode

for every tweet in tweet list:
    replace punctuation with empty string, make it all lower case (normalize)

potential_pres_tweets = []
for every lower case tweet with no punctuation:
    if regex match for present(er|ing|s|\s):
        add to potential pres tweet list

for award in award_names:
    get shortened version, store in list called shortened_awards

for tweet in potential presenter tweets:
    find index of keyword "Best"
    award_name = ""
    from index to end of list:
         if the word is in the shortened awards list and the word is not motion or picture:
            add to award name with a space
    for award in shortened awards:
        find fuzz similarity
        find award name with maximum similarity
"""