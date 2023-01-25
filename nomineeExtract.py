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

# import spacy

# def extract_entities(sentences, awardName):
#     nlp = spacy.load("en_core_web_sm") # load spaCy's pre-trained model
#     entities = []
#     for sentence in sentences:
#         if awardName in sentence:
#             doc = nlp(sentence)
#             for ent in doc.ents:
#                 if ent.label_ in ("PERSON", "MOVIE"): # check if entity is a person or movie
#                     entities.append(ent.text)
#     return entities

# sentences = ["The Golden Globe for Best Director goes to Tony Liu!",
# "I can't believe Martin Scorsese did not get Best Director!",
# "Johny Walker does not take home the Golden Globe for Best Director"]
# print(extract_entities(sentences, "Best Director"))


import spacy

import spacy

def extract_entities(text_list, award_name):
    nlp = spacy.load("en_core_web_sm")
    entities = {}
    for text in text_list:
        doc = nlp(text)
        if award_name in text:
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "MOVIE"]:
                    if ent.text in entities:
                        entities[ent.text] += 1
                    else:
                        entities[ent.text] = 1
            for token in doc:
                if token.text.istitle() and token.pos_ == "PROPN":
                    if token.text in entities:
                        entities[token.text] += 1
                    else:
                        entities[token.text] = 1
    return entities






# import chardet

# def extract_entities_from_file(file_path):
#     with open(file_path, 'rb') as f:
#         result = chardet.detect(f.read())
#     with open(file_path, encoding=result['encoding']) as f:
#         text_list = f.readlines()
#     text_list = [x.strip() for x in text_list] # remove any leading or trailing whitespaces
#     entities = extract_entities(text_list)
#     return entities


# entities = extract_entities_from_file("TweetText.txt")
# print(entities)


text_list = ["I think zac efron deserves best actor",
"adam sandler is going to get best actor",
"I hope alec smith wins best actor",
"If john doe wins best actor I will be so happy",
"Best actor should definitely go to michael jordan"]
award_name = "best actor"
entities = extract_entities(text_list, award_name)

print(entities)

