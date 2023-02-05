import re
import spacy




with open("terminatingList.txt") as f:
    excludeList = f.read().splitlines()



def nameToRegex(name: str, entity) -> list:
    names = re.split(" ", name)
    if entity == 1:
        return f"(?i).*({'|'.join(names)}).*"
    elif entity == 2:
        names = [x for x in names if x not in excludeList]
        names = "(?i)(?=.*" + ")(?=.*".join(names) + ").*"
        return names
    else:
        print(f"{entity} is Not A movie or Person!!")
    
def isPersonMovie(lst):
    nlp = spacy.load("en_core_web_sm")

    count = 0
    for name in lst:
        doc = nlp(name)
        for token in doc:
            if token.ent_type_ == "PERSON":
                count+=1
                break

    if count >=3:
        return 2
    else:
        return 1
