import re



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
    
