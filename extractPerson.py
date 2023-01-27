

import spacy
def extractPerson(sentences):
    nlp = spacy.load("en_core_web_sm")
    person_text = []
    for sentence in sentences:
        full = nlp(sentence)
        for pos in full.ents:
            if pos.label_ == "PROPN":
                person_text.append(sentence)
                break
    return person_text

list = ["I think Argo deserves best picture",
"Please give adam sandler best actor",
"I hope tom brady wins best loser",
"If john doe wins best actor I will be so happy",
"best actor should definitely go to michael jordan"]
award_name = "best picture"


people = extractPerson(list)