import spacy

def extract_entities(tweet, award):
    sp = spacy.load("en_core_web_sm")
    people = {}
    for tweet in tweets:
        doc = sp(tweet)
        if award in tweet:
            for occ in doc.ents:
                if occ.label_ in ["PERSON", "MOVIE"]:
                    if occ.text in people:
                        people[occ.text] += 1
                    else:
                        people[occ.text] = 1
            for pos in doc:
                if pos.pos_ == "PROPN":
                    if pos.text in people:
                        people[pos.text] += 1
                    else:
                        people[pos.text] = 1
    return people

tweets = open("TweetText.txt", "r", errors='ignore')

award = "best picture"
people = extract_entities(tweets, award)
print(people[0])

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
