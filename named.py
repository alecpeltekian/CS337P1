import spacy
from spacy import displacy

NER = spacy.load("en_core_web_sm")
raw_text=  "Ben Affleck wins Best Director at #GoldenGlobes. Hey Academy, fuck you"
text1= NER(raw_text)

doc = NER("hosts Tina Fey")



for word in doc.ents:
    print(word.text,word.label_)