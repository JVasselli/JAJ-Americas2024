import csv
from typing import List
import json

known_words = [
    {"token": "teen", "pos": "PRON", "lemma": "teen", "tag": "IND", "person": "1", "number": "S"},
    {"token": "teech", "pos": "PRON", "lemma": "teech", "tag": "IND", "person": "2", "number": "S"},
    {"token": "leti'", "pos": "PRON", "lemma": "leti'", "tag": "IND", "person": "3", "number": "S"},
    {"token": "to'on", "pos": "PRON", "lemma": "to'on", "tag": "IND", "person": "1", "number": "P"},
    {"token": "te'ex", "pos": "PRON", "lemma": "te'ex", "tag": "IND", "person": "2", "number": "P"},
    {"token": "leti'ob", "pos": "PRON", "lemma": "leti'ob", "tag": "IND", "person": "3", "number": "P"},

    {"token": "tene'", "pos": "PRON", "lemma": "teen", "tag": "PRP", "person": "1", "number": "S"},
    {"token": "teche'", "pos": "PRON", "lemma": "teech", "tag": "PRP", "person": "2", "number": "S"},
    {"token": "leti'e'", "pos": "PRON", "lemma": "leti'", "tag": "PRP", "person": "3", "number": "S"},
    {"token": "to'one'", "pos": "PRON", "lemma": "to'on", "tag": "PRP", "person": "1", "number": "P"},
    {"token": "te'exe'", "pos": "PRON", "lemma": "te'ex", "tag": "PRP", "person": "2", "number": "P"},
    {"token": "leti'obe'", "pos": "PRON", "lemma": "leti'ob", "tag": "PRP", "person": "3", "number": "P"},
    
    {"token": "kin", "pos": "PRON", "lemma": "in", "tag": "KA", "number": "S", "person": "1"},
    {"token": "ka", "pos": "PRON", "lemma": "a", "tag": "KA", "number": "X", "person": "2"},
    {"token": "ku", "pos": "PRON", "lemma": "u", "tag": "KA", "number": "X", "person": "3"},
    {"token": "kek", "pos": "PRON", "lemma": "k", "tag": "KA", "number": "P", "person": "1"},

    {"token": "tin", "pos": "PRON", "lemma": "in", "tag": "TA", "number": "S", "person": "1"},
    {"token": "ta", "pos": "PRON", "lemma": "a", "tag": "TA", "number": "X", "person": "2"},
    {"token": "tu", "pos": "PRON", "lemma": "u", "tag": "TA", "number": "X", "person": "3"},
    {"token": "tek", "pos": "PRON", "lemma": "k", "tag": "TA", "number": "P", "person": "1"},

    {"token": "in", "pos": "PRON", "lemma": "in", "tag": "A", "number": "S", "person": "1"},
    {"token": "a", "pos": "PRON", "lemma": "a", "tag": "A", "number": "X", "person": "2"},
    {"token": "u", "pos": "PRON", "lemma": "u", "tag": "A", "number": "X", "person": "3"},
    {"token": "k", "pos": "PRON", "lemma": "k", "tag": "A", "number": "P", "person": "1"},

    {"token": "ba'ax", "pos": "PRON", "lemma": "ba'ax", "tag": "WP"},
    {"token": "ma'ax", "pos": "PRON", "lemma": "ma'ax", "tag": "WP"},
    {"token": "tu'ux", "pos": "PRON", "lemma": "tu'ux", "tag": "WP"},
    {"token": "bix", "pos": "PRON", "lemma": "bix", "tag": "WP"},
    {"token": "bajux", "pos": "PRON", "lemma": "bajux", "tag": "WP"},
    {"token": "kux", "pos": "PRON", "lemma": "kux", "tag": "WP"},
    {"token": "máakalmáak", "pos": "PRON", "lemma": "máakalmáak", "tag": "WP"},
    {"token": "buka'aj", "pos": "PRON", "lemma": "buka'aj", "tag": "WP"},
    {"token": "ke'ex", "pos": "PRON", "lemma": "ke'ex", "tag": "WP"},
    # Discontinuous
    {"token": "ma'", "pos": "DIS", "tag": "NEG", "ending": "i'"},
    {"token": "te'", "pos": "DIS", "tag": "LOC", "ending": "o'"},
    # Adverbs from norma_maya.pdf #TODO: Real citation
    {"token": "sáamal", "pos": "ADV"},
    {"token": "náach", "pos": "ADV"},
    {"token": "séeb", "pos": "ADV"},
    {"token": "jach", "pos": "ADV"},
    {"token": "ka'abej", "pos": "ADV"},
    {"token": "naats'", "pos": "ADV"},
    {"token": "xaan", "pos": "ADV"},
    {"token": "jáan", "pos": "ADV"},
    {"token": "jo'oljeak", "pos": "ADV"},
    {"token": "aktáan", "pos": "ADV"},
    {"token": "chaambel", "pos": "ADV"},
    {"token": "chan", "pos": "ADV"},
    {"token": "ook'in", "pos": "ADV"},
    {"token": "chúumuk", "pos": "ADV"},
    {"token": "ma'alob", "pos": "ADV"},
    {"token": "k'as", "pos": "ADV"},
    {"token": "ja'atskab", "pos": "ADV"},
    {"token": "yáanal", "pos": "ADV"},
    {"token": "ya'ab", "pos": "ADV"},
    {"token": "sen", "pos": "ADV"},
    {"token": "ka'akate'", "pos": "ADV"},
    {"token": "yóok'ol", "pos": "ADV"},
    {"token": "jump'íit", "pos": "ADV"},
    {"token": "seenkech", "pos": "ADV"},
    # Verbs from norma_maya.pdf
    {"token": "noktal", "pos": "VERB"},
    {"token": "je'ankil", "pos": "VERB"},
    {"token": "buul", "pos": "VERB"},
    {"token": "janal", "pos": "VERB"},
    {"token": "jawtal", "pos": "VERB"},
    {"token": "wi'ankil", "pos": "VERB"},
    {"token": "xaktal", "pos": "VERB"},
    {"token": "iichankil", "pos": "VERB"},
    {"token": "wenel", "pos": "VERB"},
    {"token": "chintal", "pos": "VERB"},
    {"token": "lúulankil", "pos": "VERB"},
    {"token": "na'akal", "pos": "VERB"},
    {"token": "ch'ontal", "pos": "VERB"},
    {"token": "loolankil", "pos": "VERB"},
    {"token": "xook", "pos": "VERB", "type": "Ø"},
    {"token": "maan", "pos": "VERB", "type": "Ø"},
    {"token": "tóok", "pos": "VERB", "type": "Ø"},
    {"token": "chu'uch", "pos": "VERB", "type": "Ø"},
    {"token": "kóonol", "pos": "VERB", "type": "Ø"},
    {"token": "míis", "pos": "VERB", "type": "T"},
    {"token": "che'ej", "pos": "VERB", "type": "T"},
    {"token": "báaxal", "pos": "VERB", "type": "T"},
    {"token": "xuuxub", "pos": "VERB", "type": "T"},
    {"token": "k'uut", "pos": "VERB", "type": "Ø"},
    {"token": "boon", "pos": "VERB", "type": "Ø"},
    {"token": "xaab", "pos": "VERB", "type": "Ø"},
    {"token": "ch'íich'", "pos": "VERB", "type": "Ø"},
    {"token": "ja'ats'", "pos": "VERB", "type": "Ø"},
    {"token": "chaakal", "pos": "VERB", "type": "Ø"},
    {"token": "jíil", "pos": "VERB", "type": "T"},
    {"token": "tséen", "pos": "VERB", "type": "T"},
    {"token": "píib", "pos": "VERB", "type": "T"},
    {"token": "báab", "pos": "VERB", "type": "T"},
    {"token": "k'a'ay", "pos": "VERB", "type": "T"},
    {"token": "jóoyab", "pos": "VERB", "type": "T"},
    {"token": "meyaj", "pos": "VERB", "type": "T"},
    {"token": "áalkab", "pos": "VERB", "type": "T"},
    {"token": "bin", "pos": "VERB"},
    {"token": "wa'alaj", "pos": "VERB"},
    {"token": "óok'otnaj", "pos": "VERB"},
    # Adj from norma_maya.pdf
    {"token": "sak", "pos": "ADJ"},
    {"token": "tu'", "pos": "ADJ"},
    {"token": "jaay", "pos": "ADJ"},
    {"token": "tikin", "pos": "ADJ"},
    {"token": "ya'ax", "pos": "ADJ"},
    {"token": "ki'", "pos": "ADJ"},
    {"token": "kooy", "pos": "ADJ"},
    {"token": "ch'uul", "pos": "ADJ"},
    {"token": "kóom", "pos": "ADJ"},
    {"token": "su'uts'", "pos": "ADJ"},
    {"token": "polok", "pos": "ADJ"},
    {"token": "k'asa'an", "pos": "ADJ"},
    {"token": "bek'ech", "pos": "ADJ"},
    {"token": "nojoch", "pos": "ADJ"},
    {"token": "wóolis", "pos": "ADJ"},
    {"token": "k'oja'an", "pos": "ADJ"},
    {"token": "ts'oya'an", "pos": "ADJ"},
    {"token": "úuchben", "pos": "ADJ"},
    {"token": "ka'anal", "pos": "ADJ"},
    {"token": "kala'an", "pos": "ADJ"},
    # Nexos from norma_maya.pdf
    {"token": "wáaj", "pos": "NEX", "tag": "INT"},
    {"token": "yéetel", "pos": "NEX"},
    {"token": "ti'al", "pos": "NEX"},
    {"token": "uti'al", "pos": "NEX"},
    {"token": "leten", "pos": "NEX"},
    {"token": "ka'alikil", "pos": "NEX"},
    # Nouns
    {"token": "merkaado", "pos": "NOUN"},
    {"token": "áak'ab", "pos": "NOUN"},
    {"token": "ich", "pos": "NOUN"},
    {"token": "iik'", "pos": "NOUN"},
    {"token": "óol", "pos": "NOUN"},
    {"token": "k'aaba'", "pos": "NOUN"},
    {"token": "wotoch", "pos": "NOUN"},
    {"token": "koonol", "pos": "NOUN"},
    {"token": "k'íiwik", "pos": "NOUN"},
    {"token": "kool", "pos": "NOUN"},
    # Suffixes
    {"token": "imbáaj", "pos": "SUF", "tag": "RFL", "person": "1", "number": "S"},
    {"token": "abáaj", "pos": "SUF", "tag": "RFL", "person": "2", "number": "S"},
    {"token": "ubáaj", "pos": "SUF", "tag": "RFL", "person": "3", "number": "S"},
    {"token": "imba'on", "pos": "SUF", "tag": "RFL", "person": "1", "number": "P"},
    {"token": "aba'ex", "pos": "SUF", "tag": "RFL", "person": "2", "number": "P"},
    {"token": "uba'ob", "pos": "SUF", "tag": "RFL", "person": "3", "number": "P"},
    {"token": "báaj", "pos": "SUF", "tag": "RFL", "person": "1", "number": "P"},

    {"token": "en", "pos": "SUF", "tag": "PRON", "person": "1", "number": "S"},
    {"token": "ech", "pos": "SUF", "tag": "PRON", "person": "2", "number": "S"},
    {"token": "ij", "pos": "SUF", "tag": "PRON", "person": "3", "number": "S"},
    {"token": "o'on", "pos": "SUF", "tag": "PRON", "person": "1", "number": "P"},
    {"token": "on", "pos": "SUF", "tag": "PRON", "person": "1", "number": "P"},
    {"token": "o'onex", "pos": "SUF", "tag": "PRON", "person": "1", "number": "P"},
    {"token": "ox", "pos": "SUF", "tag": "PRON", "person": "1", "number": "P"}, # from Maya0317
    {"token": "e'ex", "pos": "SUF", "tag": "PRON", "person": "2", "number": "P"},
    {"token": "ex", "pos": "SUF", "tag": "PRON", "person": "2", "number": "P"},
    {"token": "o'ob", "pos": "SUF", "tag": "PRON", "person": "3", "number": "P"},
    {"token": "'ob", "pos": "SUF", "tag": "PRON", "person": "3", "number": "P"},
    # AUX and PART
    #{"token": "tan", "pos": "AUX", "tag": "CONT"},
    {"token": "káaj", "pos": "ASP", "tag": "BEG"},
    {"token": "yaan", "pos": "ASP", "tag": "COM"},
    {"token": "suuk", "pos": "ASP", "tag": "CUS"},
    {"token": "taak", "pos": "ASP", "tag": "DES"},
    {"token": "táant", "pos": "ASP", "tag": "IMM", "ending": "e'"},
    {"token": "je'el", "pos": "ASP", "tag": "INS", "ending": "e'"},
    {"token": "k'a'abéet", "pos": "ASP", "tag": "OBL"},
    {"token": "táan", "pos": "ASP", "tag": "PRG"},
    {"token": "ts'o'ok", "pos": "ASP", "tag": "TER"},
    {"token": "jo'op'", "pos": "ASP", "tag": "UNK"},
    #{"token": "te'elo'", "pos": "PART", "tag": "LOC"}
]

known_suffixes = [t for t in known_words if t["pos"] == "SUF"]

def check_if_known(token):
    for known in known_words:
        if known["token"] == token:
            return known

class MayaToken:
    def __init__(self, token, pos="", tag="", number="", person="", aspect="", ending=""):
        self.token = token
        self.pos = pos
        self.lemma = token.lower()
        self.tag = tag
        self.number = number
        self.person = person
        self.aspect = aspect
        self.ending = ending
        self.suffix = ""

        if token.islower():
            self.shape = "xx"
        elif token.isupper():
            self.shape = "XX"
        else:
            self.shape = "Xx"

        if not self.pos:
            self.populate_if_known()
        if not self.person and not self.number:
            self.deconjugate()
        
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"{self.token} ({self.detailed_pos()})"
    
    def detailed_pos(self):
        sub_pos = f"{self.person}_{self.number}" if self.person != "" else ""
        return f"{self.pos}:{self.tag}:{sub_pos}"
    
    def update_word(self, new_token, new_pos, new_tag):
        self.token = new_token
        self.lemma = new_token
        self.to_shape(self.shape)
        self.pos = new_pos
        self.tag = new_tag
    
    def deconjugate(self):
        for suffix in known_suffixes:
            if self.lemma.endswith(suffix["token"]):
                self.person = suffix["person"]
                self.number = suffix["number"]
                self.lemma = self.lemma[:-len(suffix["token"])]
                self.tag = self.lemma
                self.suffix = suffix["token"]
                break
        
        if self.lemma.endswith("naj"):
            self.lemma = self.lemma[:-3]
            self.pos = "VERB"
            self.tag = self.lemma + "-naj"

        if not self.pos:
            self.populate_if_known()
    
    def populate_if_known(self):
        possible_token = check_if_known(self.lemma)
        if possible_token:
            self.pos = possible_token["pos"] if "pos" in possible_token else ""
            self.lemma = possible_token["lemma"] if "lemma" in possible_token else self.lemma
            self.tag = possible_token["tag"] if "tag" in possible_token else self.tag
            self.number = possible_token["number"] if "number" in possible_token else self.number
            self.person = possible_token["person"] if "person" in possible_token else self.person
            self.aspect = possible_token["aspect"] if "aspect" in possible_token else self.aspect
            self.ending = possible_token["ending"] if "ending" in possible_token else self.ending

    def to_shape(self, new_shape):
        self.shape = new_shape
        if self.shape == "xx":
            self.token = self.token.lower()
        elif self.shape == "XX":
            self.token = self.token.upper()
        elif len(self.token) > 1:
            self.token = self.token[0].upper() + self.token[1:].lower()

    def to_person_number(self, person, number):
        if person == self.person and number == self.number:
            return self
        
        if self.pos == "PRON" and self.tag != "WP":
            possible_pronouns = [w for w in known_words if w.get("pos") == "PRON" and w.get("tag", "") == self.tag and w.get("person") == person and w.get("number") in [number, "X"]]
            print(possible_pronouns)
            new_token = MayaToken(**possible_pronouns[0])
            new_token.to_shape(self.shape)
            return new_token

        if self.pos == "VERB" and self.person == "":
            try:
                possible_suffix = [w for w in known_suffixes if w.get("person") == person and w.get("number") == number and w.get("tag") == "PRON"][0]
                new_token = MayaToken(self.lemma + possible_suffix["token"], pos=self.pos, lemma=self.lemma, tag=self.tag, number=number, person=person)
                new_token.to_shape(self.shape)
                return new_token
            except:
                print("Unable to find possible suffix", person, number, self)
                return self

        if self.pos in ["NOUN", ""] and self.person != "" and self.number != "": #removed VERB
            try:
                current_suffix = [w for w in known_suffixes if w.get("token") == self.token[len(self.lemma):]][0]
            except:
                print("Unable to find current suffix", self.token[len(self.lemma):])
                return self
            
            if person == "3" and number == "S" and current_suffix["tag"] == "PRON":
                #This is the case where just returning the lemma should work
                return MayaToken(self.lemma, pos=self.pos, lemma=self.lemma, tag=self.tag, number=number, person=person)
            
            try:
                possible_suffix = [w for w in known_suffixes if w.get("person") == person and w.get("number") == number and w.get("tag") == current_suffix.get("tag")][0]
                new_token = MayaToken(self.lemma + possible_suffix["token"], pos=self.pos, lemma=self.lemma, tag=self.tag, number=number, person=person)
                new_token.to_shape(self.shape)
                return new_token
            except:
                print("Unable to find possible suffix", person, number, current_suffix.tag)
                return self

        return self
        
def pos_tag_maya(sentence: str) -> str:
    tagged = pos_tag(sentence)
    return " ".join([f"({t.token}, {t.detailed_pos()})" for t in tagged])

def pos_tag(sentence: str) -> List[MayaToken]:
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
    discontiuous = None
    for i, token in enumerate(tokens):
        token = MayaToken(token)
        pos_tagged.append(token)

        if token.pos == "DIS" or token.ending != "":
            discontiuous = token
            continue

        if i == len(tokens) - 1 and discontiuous:
            if token.token.endswith(discontiuous.ending):
                #token.tag = discontiuous.tag
                token.lemma = token.lemma[:-len(discontiuous.ending)]
                token.token = token.token[:-len(discontiuous.ending)]
                token.deconjugate()
                #discontiuous = None
                ending = MayaToken(discontiuous.ending, pos="END", tag=discontiuous.tag)
                pos_tagged.append(ending)
        
    return pos_tagged

replacement_changes = {
    "ASPECT:BEG, TENSE:PAS_SIM": "ASPECT:BEG",
    "ASPECT:COM, TENSE:FUT_SIM": "ASPECT:COM",
    "ASPECT:CUS, TENSE:PRE_SIM": "ASPECT:CUS",
    "ASPECT:HAB, TENSE:PRE_SIM": "ASPECT:HAB",
    "ASPECT:IMM, TENSE:PAS_SIM": "ASPECT:IMM",
    "ASPECT:INS, TENSE:FUT_SIM": "ASPECT:INS",
    "ASPECT:OBL, TENSE:FUT_SIM": "ASPECT:OBL",
    "ASPECT:TER, TENSE:PAS_SIM": "ASPECT:TER",
}

def convert_changes_maya(changes):
    for key in replacement_changes:
        changes = changes.replace(key, replacement_changes[key])
    changes = [c for c in changes.split(", ") if "TENSE" not in c]
    #Order: STATUS -> PERSON -> ASPECT -> TYPE -> SUBTYPE
    changes = sorted(changes, key=lambda x: ["STATUS", "PERSON", "ASPECT", "TYPE", "SUBTYPE"].index(x.split(":")[0]))
    return changes

with open("../ref/maya_info.json", "r") as f:
    maya_info = json.load(f)

def hint_from_change_maya(change):
    if change in maya_info:
        return maya_info[change]
    return ""
    

"""def change_aspect(tagged, new_aspect): #TODO: If wáaj... HAB = KA, NN, wáaj, other aspects = ASP, wáaj, PRON:A, NN
    #check if "wáaj" exists in the sentence
    is_question = False
    if "wáaj" in [x.token for x in tagged]:
        #remove
        tagged = [x for x in tagged if x.token != "wáaj"]
        is_question = True

    if "ASP" in [x.tag for x in tagged]:
        index = [x.tag for x in tagged].index("ASP")
        tagged[index].update_word(new_aspect, "PART", "ASP")
    elif "KA" in [x.tag for x in tagged]:
        index = [x.tag for x in tagged].index("KA")
        person = tagged[index].person
        number = tagged[index].number
        tagged[index].update_word(new_aspect, "PART", "ASP")
        new_pron = [x for x in known_words if x.get("pos") == "PRON" and x.get("tag") == "A" and x.get("person") == person and x.get("number") in [number, "X"]][0]
        new_pron = MayaToken(**new_pron)
        new_pron.to_shape("xx")
        #insert after tagged[index]
        tagged = tagged[:index+1] + [new_pron] + tagged[index+1:]

    if is_question == True:
        tagged = tagged[:index+1] + [MayaToken("wáaj", pos="NEX", tag="INT")] + tagged[index+1:]
    
    return tagged

def remove_aspect(tagged):
    #All aspect become KA pronoun.  Look at the next word to determine person and number
    if "ASP" in [x.tag for x in tagged]:
        index = [x.tag for x in tagged].index("ASP")
        #Check if the next token is wáaj
        is_question = False
        if tagged[index+1].token == "wáaj":
            #temporarily remove wáaj
            tagged = tagged[:index+1] + tagged[index+2:]
            is_question = True
        person = tagged[index+1].person
        number = tagged[index+1].number
        new_pron = [x for x in known_words if x.get("pos") == "PRON" and x.get("tag") == "KA" and x.get("person") == person and x.get("number") in [number, "X"]][0]
        new_pron = MayaToken(**new_pron)
        new_pron.to_shape(tagged[index].shape)
        tagged = tagged[:index] + [new_pron] + tagged[index+2:]
        if is_question:
            tagged = tagged[:index+2] + [MayaToken("wáaj", pos="NEX", tag="INT")] + tagged[index+2:]
    return tagged



def change_tagged_sentence(tagged, person=None, number=None, is_question=False, is_negative=False, aspect=False, verbose=False):
    #if is_question and tagged pos is PRON, PRON replace the first with Bix and remove END (if applicable)
    #if is_neg, add Ma' to beginning of sentence, and i' at end of sentence (remove e' END if applicable)
    new_tokens = []

    # Bix
    if is_question and len(tagged) > 2 and len(tagged) < 4 and tagged[0].pos == "PRON" and tagged[1].pos == "PRON":
        new_token = MayaToken("bix", pos="PRON", lemma="bix", tag="WP")
        new_token.to_shape(tagged[0].shape)
        new_tokens.append(new_token)
        tagged = tagged[1:]
        if tagged[-1].pos == "END":
            tagged = tagged[:-1]
        is_question = False

    # remove leading personal pronouns (Teche')
    #Had is_question here, but I think that's only for Bix
    if is_negative and tagged[0].pos == "PRON" and "B" in tagged[0].tag:
        tagged[1].to_shape(tagged[0].shape)
        tagged = tagged[1:]

    # Figure out where to Ma'
    if is_negative:
        if tagged[0].tag != "B.e'":
            new_tokens.append(MayaToken("Ma'", pos="DIS", tag="NEG", ending="i'"))
            tagged[0].to_shape("xx")
        else:
            ma = MayaToken("ma'", pos="DIS", tag="NEG", ending="i'")
            tagged = tagged[:1] + [ma] + tagged[1:]

        if tagged[-1].pos == "END":
            tagged = tagged[:-1]
        if not tagged[-1].token.endswith("i'"):
            tagged.append(MayaToken("i'", pos="END", tag="NEG"))

        is_negative = False

        # When a negative/question Ma' wáaj is normal
        if is_question:
            # Nouns slot between Ma' and wáaj
            if tagged[0].pos == "NOUN":
                new_tokens.append(tagged[0])
                tagged = tagged[1:]

            new_tokens.append(MayaToken("wáaj", pos="NEX", tag="INT"))
            is_question = False

    if aspect == "DES":
        tagged = change_aspect(tagged, "taak")
    elif aspect == "OBL":
        tagged = change_aspect(tagged, "k'a'abéet")
    elif aspect == "BEG":
        tagged = change_aspect(tagged, "káaj")
    elif aspect == "COM":
        tagged = change_aspect(tagged, "yaan")
    elif aspect == "CUS":
        tagged = change_aspect(tagged, "suuk")
    elif aspect == "IMM":
        tagged = change_aspect(tagged, "táant")
    elif aspect == "INS":
        tagged = change_aspect(tagged, "je'el")
    elif aspect == "PRG":
        tagged = change_aspect(tagged, "táan")
    elif aspect == "TER":
        tagged = change_aspect(tagged, "ts'o'ok")
    elif aspect == "HAB":
        tagged = remove_aspect(tagged)

    ###
    if tagged[0].detailed_pos() == "PART:ASP" and person and number:
        print("Looking for a personal pronoun")
        #try:
        #find the correct personal pronoun and capitalize it
        new_token = [x for x in known_words if x.get("tag") == "B.e'" and x.get("person") == person and x.get("number") in [number, "X"]][0]
        new_token = MayaToken(**new_token)
        new_token.to_shape("Xx")
        new_tokens.append(new_token)
        tagged[0].to_shape("xx")
        #except:
        #    pass
        #uncapitalize the táan###

    #Loop through the rest of the sentence
    for token in tagged:
        if person and number:
            new_token = token.to_person_number(person, number) #TODO make sure this only happen for the first PRON and first 1 or 2
            if token.person != "" and token.number != "" and token.pos in ["", "NOUN", "VERB"]: # only change the first verb or noun
                person = None
                number = None
        else:
            new_token = token

        new_tokens.append(new_token)

        if is_question and token.pos in ["VERB", "NOUN", "PART", ""]:
            new_tokens.append(MayaToken("wáaj", pos="NEX", tag="INT"))
            is_question = False

    if verbose:
        print(new_tokens)

    new_sentence = ""
    for i, token in enumerate(new_tokens):
        prev_token = new_tokens[i-1] if i > 0 else None

        if person and number and prev_token and prev_token.pos == "PRON" and prev_token.tag in ["A", "TA"] and token.token[0] in ["y", "w"]:
            if prev_token.person == "1":
                #token.token = "w" + token.token[1:]
                token.token = token.token[1:]
            elif prev_token.person == "2":
                token.token = "w" + token.token[1:]
            elif prev_token.person == "3":
                token.token = "y" + token.token[1:]

        if token.pos == "END":
            new_sentence += token.token
        else:
            new_sentence += " " + token.token

    return new_sentence.strip()

def test_one(id, data):
    item = [d for d in data if d["ID"] == id][0]
    print(item)
    print(pos_tag(item["Source"]))
    print(pos_tag(item["Target"]))

    change_segments = item["Change"].split(", ")
    is_question = False
    is_negative = False
    aspect = False
    person = None
    number = None
    for segment in change_segments:
        if "PERSON:" in segment:
            person = segment.split(":")[1].split("_")[0]
            number = segment.split(":")[1].split("_")[1][0]
        if "SUBTYPE:INT" in segment:
            is_question = True
        if "TYPE:NEG" in segment:
            is_negative = True
        if "ASPECT:" in segment:
            aspect = segment.split(":")[1]

    changed = change_tagged_sentence(pos_tag(item["Source"]), person=person, number=number, is_question=is_question, is_negative=is_negative, aspect=aspect, verbose=True)
    item["Predicted Target"] = changed
    print(changed, "!!!!!!!!" if changed == item["Target"] else "")


def loop_through_data(data, slow_mode=True):
    for d in data:
        d["Length"] = len(d["Source"].split())

    #sort by length (smallest to largest)
    #data = sorted(data, key=lambda x: x["Length"])
    for item in data:
        print(item)
        print(pos_tag(item["Source"]))
        #print(pos_tag(item["Target"]))

        change_segments = item["Change"].split(", ")
        is_question = False
        is_negative = False
        aspect = False
        person = None
        number = None
        for segment in change_segments:
            if "PERSON:" in segment:
                person = segment.split(":")[1].split("_")[0]
                number = segment.split(":")[1].split("_")[1][0]
            if "SUBTYPE:INT" in segment:
                is_question = True
            if "TYPE:NEG" in segment:
                is_negative = True
            if "ASPECT:" in segment:
                aspect = segment.split(":")[1]

        changed = change_tagged_sentence(pos_tag(item["Source"]), person=person, number=number, is_question=is_question, is_negative=is_negative, aspect=aspect)
        item["Predicted Target"] = changed
        print(changed, "!!!!!!!!" if changed == item["Target"] else "")
        #if any([(token.pos == "" and token.person == "") for token in pos_tag(item["Source"])]):
        if slow_mode and input() == "stop":
            break

    with open("../results/manual/maya-dev-prediction.tsv", "w") as csvfile:
        fieldnames = ["ID", "Source", "Target", "Change", "Predicted Target", "Length"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for item in data:
            writer.writerow(item)
"""
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def get_sentence_template(sentence, level=1):
    tagged = pos_tag(sentence.lower())
    sentence_template = ""
    curr_letter = 0
    for word in tagged:
        if word.pos in ["PRON", "DIS", "ASP", "NEX"]:
            if level == 1:
                sentence_template += word.token + " "
            else:
                sentence_template += word.pos + ":" + word.tag + " "
            continue

        if word.pos != "END":
            sentence_template += letters[curr_letter] if level < 3 else ""
            curr_letter += 1
        
            if word.suffix != "":
                if level == 1:
                    sentence_template += "-" + word.suffix
                elif level == 2:
                    sentence_template += "-" + word.person + "_" + word.number
                else:
                    sentence_template += "PRON:SUFF"

        elif level == 1:
            sentence_template = sentence_template.strip()
            if word.token == "i'":
                sentence_template += "-i'"
            if word.token == "e'":
                sentence_template += "-e'"

        sentence_template += " "
    return sentence_template.strip()

def similarity_score(source1, source2):
    if source1 == source2:
        return 1
    template1 = get_sentence_template(source1, level=1)
    template2 = get_sentence_template(source2, level=1)
    if template1 == template2:
        return 0.8
    
    template1 = get_sentence_template(source1, level=2)
    template2 = get_sentence_template(source2, level=2)
    if template1 == template2:
        return 0.7
    
    template1 = get_sentence_template(source1, level=3)
    template2 = get_sentence_template(source2, level=3)
    if template1 == template2:
        return 0.6
    
    components1 = set(template1.split(" "))
    components2 = set(template2.split(" "))
    #how many overlap normalized by how many exist
    overlap = len(components1.intersection(components2))
    total = len(components1.union(components2))
    if overlap == 0:
        return 0
    return overlap/total * 0.5
