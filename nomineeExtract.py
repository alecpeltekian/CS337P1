# import spacy

# def extract_entities(tweets, award):
#     sp = spacy.load("en_core_web_sm")
#     people = {}
#     for tweet in tweets:
#         doc = sp(tweet)
#         if award in tweet:
#             for occ in doc.ents:
#                 if occ.label_ in ["MOVIE"]:
#                     if occ.text in people:
#                         people[occ.text] += 1
#                     else:
#                         people[occ.text] = 1
#             for pos in doc:
#                 if pos.pos_ == "PROPN":
#                     if pos.text in people:
#                         people[pos.text] += 1
#                     else:
#                         people[pos.text] = 1
#     return people

# tweets = open("winnerTweets.txt", "r", errors='ignore')

# # list = ["I think Argo deserves best picture",
# # "Please give adam sandler best actor",
# # "I hope tom brady wins best loser",
# # "If john doe wins best actor I will be so happy",
# # "best actor should definitely go to michael jordan"]

# award = "best drama"
# people = extract_entities(tweets, award)
# #print(people)

# import operator
# sorted_d = dict( sorted(people.items(), key=operator.itemgetter(1),reverse=True))
# print(list(sorted_d)[:15])

# def textSplit(entities):
#     with open('nomineeExtract.txt', 'w', errors='ignore') as output:
#         for index in range(len(entities)):
#             for key in entities[index]:
#                 if key == 'text':
#                     text = entities[index][key]
#                     output.write('   ')
#                     output.write(text)
#                     output.write('\r')



# print(textSplit(data))


# import spacy

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Please give Adam Sandler best actor")

# for token in doc:
#     if token.pos_ == "NOUN":
#         print(token.text)



import spacy

# def remove_wo_person(text_list):
#     nlp = spacy.load("en_core_web_sm")
#     modified_text_list = []
#     for tweet in text_list:
#         doc = nlp(tweet)
#         for ent in doc.ents:
#             if ent.label_ == "PERSON":
#                 modified_text_list.append(tweet)
#                 break
#     return modified_text_list


# text_list = ["John Smith won", "The Shawshank Redemption is a 1994 American drama film"]

# modified_text_list_1 = remove_wo_person(text_list)
# print(modified_text_list_1)


import spacy

nlp = spacy.load("en_core_web_sm")

def remove_wo_movie(tweet_list):
    modified_text_list = []
    for tweet in tweet_list:
        doc = nlp(tweet)
        if not any(ent.label_ == "MOVIE" for ent in doc.ents):
            modified_text_list.append(tweet)
    return modified_text_list


text_list = ["John Smith won", "Shrek is my favorite movie"]

modified_text_list_1 = remove_wo_movie(text_list)
print(modified_text_list_1)
