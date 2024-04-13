import json

known_words = [
    {"token": "ye'", "pos": "PRON", "person": "1_SI"},
    {"token": "be'", "pos": "PRON", "person": "2_SI"},
    {"token": "ie'", "pos": "PRON", "person": "3_SI"},
    {"token": "sa'", "pos": "PRON", "person": "1_PL_EXC"},
    {"token": "se'", "pos": "PRON", "person": "1_PL_INT"},
    {"token": "a'", "pos": "PRON", "person": "2_PL"},
    {"token": "ie'pa", "pos": "PRON", "person": "3_PL"},
    #Weak forms
    {"token": "ya", "pos": "PRON", "person": "1_SI"},
    {"token": "ba", "pos": "PRON", "person": "2_SI"},
    {"token": "ma", "pos": "PRON", "person": "2_SI"},
    {"token": "i", "pos": "PRON", "person": "3"},
    {"token": "sa", "pos": "PRON", "person": "1_PL_EXC"},
    {"token": "a", "pos": "PRON", "person": "2_PL"},

    {"token": "tso", "pos": "VERB"},

    {"token": "i'", "pos": "DEM"},
    {"token": "e'", "pos": "DEM"},
    {"token": "wa", "pos": "INST"},
    {"token": "kë̀", "pos": "NEG"},
    {"token": "tö", "pos": "ERG"},
    {"token": "r", "pos": "ERG"},
    {"token": "rö", "pos": "ERG"},
    {"token": "dör", "pos": "COP"},
    {"token": "wa̠", "pos": "AG"},
    {"token": "ta̠", "pos": "PROG"},
]

def load_pos_dictionary():
    dictionary = json.load(open("../ref/bribri_dic.json"))
    dictionary = {entry["lema"]: entry for entry in dictionary}
    pos_dict = {}
    for lema, entry in dictionary.items():
        if ", " in lema and "cat" in entry:
            for token in lema.split(", "):
                pos_dict[token.strip()] = entry["cat"]

        if "cat" in entry:
            pos_dict[lema] = entry["cat"]
        elif "rem" in entry and "cat" in dictionary[entry["rem"]]:
            pos_dict[lema] = dictionary[entry["rem"]]["cat"]
    return pos_dict

pos_dict = load_pos_dictionary()

def check_if_known(token):
    for known in known_words:
        if known["token"] == token:
            return known
    if token in pos_dict:
        return {"token": token, "pos": pos_dict[token]}


class BribriToken:
    def __init__(self, token, pos="", person=""):
        self.token = token
        self.pos = pos
        self.person = person

        if token.islower():
            self.shape = "xx"
        elif token.isupper():
            self.shape = "XX"
        else:
            self.shape = "Xx"

        if not self.pos:
            self.populate_if_known()

        
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"{self.token} ({self.detailed_pos()})"
    
    def detailed_pos(self):
        if self.person != "":
            return f"{self.pos}:{self.person}"
        return f"{self.pos if self.pos else 'UNK'}"
    
    def update_word(self, new_token, new_pos):
        self.token = new_token
        self.to_shape(self.shape)
        self.pos = new_pos
    
    def populate_if_known(self):
        possible_token = check_if_known(self.token.lower())
        if possible_token:
            self.pos = possible_token["pos"] if "pos" in possible_token else ""
            self.person = possible_token["person"] if "person" in possible_token else self.person
            
def pos_tag_bribri(sentence: str) -> str:
    tagged = pos_tag(sentence)
    return " ".join([f"({t.token}, {t.detailed_pos()})" for t in tagged])

def pos_tag(sentence: str):
    """
    Tokenizes and tags the sentence with POS tags
    Arguments:
    sentence: str - The sentence to tag
    Returns:
    List[MayaToken] - A list of MayaTokens
    """
    #split the sentence into tokens
    tokens = sentence.split()
    pos_tagged = []
    for token in tokens:
        token = BribriToken(token)
        pos_tagged.append(token)

    #if there's no VERB or COP, mark last pos == "" as VERB
    if not any([token.pos == "VERB" or token.pos == "COP" for token in pos_tagged]):
        for token in reversed(pos_tagged):
            if token.pos == "":
                token.pos = "VERB"
                break
            if token.token.endswith("'"):
                token.pos = "VERB"
                break

    return pos_tagged

def verb_in_source(sentence):
    tagged = pos_tag(sentence)
    for token in reversed(tagged):
        if token.pos == "VERB":
            return token.token
    return None

replacement_changes = {
    "ABSNUM:PL, PERSON:1_PL_EXC": "PERSON:1_PL_EXC",
    "ABSNUM:PL, PERSON:1_PL_INC": "PERSON:1_PL_INC",
    "ABSNUM:PL, PERSON:2_PL": "PERSON:2_PL",
    "ABSNUM:PL, PERSON:3_PL": "PERSON:3_PL",
    "ABSNUM:NI, PERSON:NA": "PERSON:NA",
    "VOICE:MID, PERSON:NA": "VOICE:MID",
    "VOICE:MID, PERSON:3_SI": "VOICE:MID",
}

def convert_changes_bribri(changes):
    for key in replacement_changes:
        changes = changes.replace(key, replacement_changes[key])

    if "PERSON" in changes and not changes.startswith("PERSON"):
        first_half = changes.split(", PERSON")[0]
        second_half = "PERSON" + changes.split("PERSON")[1]
        return [first_half, second_half]
    
    return [changes]

with open("../ref/bribri_info.json", "r") as f:
    bribri_info = json.load(f)

def hint_from_change_bribri(changes):
    hint = ""
    for change in changes.split(", "):
        if change in bribri_info:
            hint += bribri_info[change] + "\n"
    return hint
