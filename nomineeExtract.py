# import re
# from collections import Counter

# def get_name_counts(tweets, award_name):
#     names = []
#     for tweet in tweets:
#         # Use regular expressions to search for the award name and any capitalized words after it
        
#         match = re.findall(r'\b([A-Z][a-z]+)\b', tweet)
#         if match:
#             for m in match:
#                 if award_name not in m:
#                     names.append(m)
#     # Use the Counter class to count the occurrences of each name
#     name_counts = Counter(names)
#     return name_counts




# tweets = [
#     "The Golden Globe for Best Director goes to Martin Scorsese for The Irishman!",
#     "I can't believe Martin Scorsese won the Golden Globe for Best Director! #TheIrishman",
#     "Martin Scorsese's The Irishman takes home the Golden Globe for Best Director"
# ]
# award_name = "Golden Globe for Best Director"
# name_counts = get_name_counts(tweets, award_name)
# print(name_counts)

import spacy

def extract_entities(sentences, awardName):
    nlp = spacy.load("en_core_web_sm") # load spaCy's pre-trained model
    entities = []
    for sentence in sentences:
        if awardName in sentence:
            doc = nlp(sentence)
            for ent in doc.ents:
                if ent.label_ in ("PERSON", "MOVIE"): # check if entity is a person or movie
                    entities.append(ent.text)
    return entities

sentences = ["The Golden Globe for Best Director goes to Tony Liu!",
"I can't believe Martin Scorsese did not get Best Director!",
"Johny Walker does not take home the Golden Globe for Best Director"]
print(extract_entities(sentences, "Best Director"))
