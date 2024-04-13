#Read the bribri_verbs.csv file and store it in a dictionary
#Make a function or class that can be used to access the data in the dictionary
#it should look up verbs in REM activo mode and return the row
#There should be another that returns the correct conjugation

import pandas as pd
from verb_utils import find_last_vowel, replace_last, add_accent_to_last_vowel, remove_last_accent
import json

#iterator for the bribriverbDB
class BribriVerbIter:
    def __init__(self, verb_db):
        self.verb_db = verb_db
        self.verb_list = list(verb_db.get_all_verbs())
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.verb_list):
            verb = self.verb_list[self.index]
            self.index += 1
            return verb
        else:
            raise StopIteration


class BribriVerbDatabase:
    def __init__(self):
        file_name = "../ref/bribri_verbs.csv"
        self.verb_df = pd.read_csv(file_name)
        self.verb_df = self.verb_df.fillna("")
        #Glosa, INF activo, IMP activo, REM activo, IMP medio, REM medio, verb type
        self.verb_dict = {}
        for _, row in self.verb_df.iterrows():
            self.verb_dict[row['REM activo']] = {
                "INF_ACT" : row['INF activo'],
                "IMP_ACT" : row['IMP activo'],
                "REM_ACT" : row['REM activo'],
                "REC_ACT" : row['REC activo'],
                "IMP_MID" : row['IMP medio'],
                "REM_MID" : row['REM medio'],
                "verb_type" : row['verb type']
            }
            self.verb_dict[row['INF activo']] = self.verb_dict[row['REM activo']]
            self.verb_dict[row['IMP activo']] = self.verb_dict[row['REM activo']]
            self.verb_dict[row['REC activo']] = self.verb_dict[row['REM activo']]
            self.verb_dict[row['IMP medio']] = self.verb_dict[row['REM activo']]
            self.verb_dict[row['REM medio']] = self.verb_dict[row['REM activo']]

        self.verb_trie = {}
        self.setup_trie()

    def setup_trie(self):
        for verb in self.verb_dict:
            node = self.verb_trie
            for letter in verb:
                if letter not in node:
                    node[letter] = {}
                node = node[letter]
            node["END"] = verb

    def find_verb_with_trie(self, verb):
        node = self.verb_trie
        verb_so_far = ""
        for letter in verb:
            if letter not in node:
                no_accent = remove_last_accent(letter)
                if no_accent in node:
                    verb_so_far += no_accent
                    return self.finish_from_node(node[no_accent])
                return None
            node = node[letter]
            verb_so_far += letter
        return node["END"] if "END" in node else None
    
    def finish_from_node(self, node):
        if "END" in node:
            return node["END"]
        if "'" in node:
            return self.finish_from_node(node["'"])
        return self.finish_from_node(node.values()[0])
    
    def __iter__(self):
        return BribriVerbIter(self)

    def get_verb(self, verb):
        if verb not in self.verb_dict and (verb.endswith("rë") or verb.endswith("dë")):
            verb = verb[:-2]

        if verb not in self.verb_dict and verb.endswith("a'"):
            base = verb[:-2]
            self.verb_dict[verb] = {
                "INF_ACT" : base + "ö́k",
                "IMP_ACT" : base + "ö̀",
                "REM_ACT" : verb,
                "REC_ACT" : base + "é",
                "IMP_MID" : base + "àr",
                "REM_MID" : base + "àne̠",
                "verb_type" : "i.o.r"
            }
            return self.verb_dict[verb]
        
        if verb not in self.verb_dict and verb.endswith("e̠'"):
            base = verb[:-3]
            self.verb_dict[verb] = {
                "INF_ACT" : base + "u̠k",
                "IMP_ACT" : base + "è̠",
                "REM_ACT" : verb,
                "REC_ACT" : base + "é̠",
                "IMP_MID" : base + "è̠r",
                "REM_MID" : base + "è̠ne̠",
                "verb_type" : "t.n.r"
            }
            return self.verb_dict[verb]

        if verb not in self.verb_dict:
            return None

        return self.verb_dict[verb]

    def get_base_conjugation(self, verb, voice="ACT", tense="REM"):
        verb_row = self.get_verb(verb)
        if verb_row is None:
            return verb
        
        conjugated_form = verb_row[tense + "_" + voice].strip()
        if voice == "MID" and tense == "IMP" and conjugated_form == "":
            conjugated_form = verb_row["REM_MID"].strip()[:-3] + "r"

        if conjugated_form is None or conjugated_form == "":
            return verb
        else:
            return conjugated_form
    
    def active_suffix(self, verb):
        if verb.endswith("rë"):
            return "rö"
        elif verb.endswith("dë"):
            return "dö"
        return ""
    
    def middle_suffix(self, verb):
        if verb.endswith("rë"):
            return "re"
        elif verb.endswith("dë"):
            return "de"
        return ""
    
    def conjugate_active(self, verb, oral_ending, nasal_ending, base="IMP", with_replacement=True):
        suffix = self.active_suffix(verb)
        conjugation = self.get_base_conjugation(verb, tense=base)
        if base == "INF":
            for e in ["ùk", "ù̠k", "ú̠k", "u̠k", "uk"]:
                if e in conjugation:
                    if with_replacement:
                        return replace_last(conjugation, e, nasal_ending) + suffix
                    else:
                        return replace_last(conjugation, e, e + nasal_ending) + suffix
            for e in ["ö̀k", "ö́k"]:
                if e in conjugation:
                    if with_replacement:
                        return replace_last(conjugation, e, oral_ending) + suffix
                    else:
                        return replace_last(conjugation, e, e + oral_ending) + suffix
        if base == "IMP":
            for e in ["è̠"]:
                if e in conjugation:
                    if with_replacement:
                        return replace_last(conjugation, e, nasal_ending) + suffix
                    else:
                        return replace_last(conjugation, e, e + nasal_ending) + suffix
            for e in ["è", "ö̀", "ö"]:
                if e in conjugation:
                    if with_replacement:
                        return replace_last(conjugation, e, oral_ending) + suffix
                    else:
                        return replace_last(conjugation, e, e + oral_ending) + suffix
        return conjugation
    
    def conjugate_middle(self, verb, ending):
        suffix = self.middle_suffix(verb)
        conjugation = self.get_base_conjugation(verb, voice="MID", tense="IMP")
        remote = self.get_base_conjugation(verb, voice="MID", tense="REM")
        if conjugation is None:
            return remote if remote is not None else verb
        
        return replace_last(conjugation, "r", ending) + suffix
    
    def get_mode_des(self, verb):
        des = self.conjugate_active(verb, "a'ku̠", "a̠'ku̠")
        if des.endswith("ku̠wa̠"):
            return replace_last(des, "ku̠wa̠", "kwa̠")
        return des

    def get_mode_imp(self, verb, type="POS", voice="ACT"):
        if type == "POS":
            return self.conjugate_active(verb, "ö́", "ú̠", base="INF")
        if type == "NEG" and voice == "ACT":
            return self.conjugate_active(verb, "ök", "u̠k", base="INF")

        return self.conjugate_active(verb, "ar", "a̠r")
    
    def get_mode_exh(self, verb):
        return self.conjugate_active(verb, "ö̀", "ú̠", base="INF")
    
    def get_mode_advers(self, verb):
        return self.conjugate_active(verb, "a'", "a̠'")
    
    def get_mode_pot(self, verb, type="POS"):
        is_transitive = self.get_verb(verb)["verb_type"].startswith("t")
        if not is_transitive:
            if type == "POS":
                conjugation = self.conjugate_active(verb, "ó", "ó̠")
            else:
                conjugation = self.conjugate_active(verb, "o", "o̠")
        else:
            conjugation = add_accent_to_last_vowel(verb, "/")
            conjugation = replace_last(conjugation,"'", "")

        start, _ = find_last_vowel(conjugation)
        if start < 3:
            conjugation += "r"
        return conjugation
    
    def get_mode_pasplu(self, verb):
        suffix = self.middle_suffix(verb)
        verb = self.get_base_conjugation(verb, tense="IMP", voice="MID")
        verb = remove_last_accent(verb)
        verb = add_accent_to_last_vowel(verb, "/")
        return verb + "ule" + suffix
    
    def get_mode_futcer(self, verb, voice="ACT", type="POS"):
        #FUT_CER
        if voice == "ACT" or self.get_verb(verb)["verb_type"] == "t.n.i":
            conjugation = "râ" if type == "POS" else "pa"
            return self.conjugate_active(verb, conjugation, conjugation, with_replacement=False)
        else:
            return self.conjugate_middle(verb, "rdâ" if type == "POS" else "rpa")
    
    def get_mode_hab(self, verb, voice="ACT", type="POS"):
        conjugation = "ke̠" if type == "POS" else "ku̠"
        if voice == "ACT" or self.get_verb(verb)["verb_type"] == "t.n.i":
            return self.conjugate_active(verb, conjugation, conjugation, with_replacement=False)
        else:
            return self.conjugate_middle(verb, "r" + conjugation)

    def get_mode_futpot(self, verb, voice="ACT", type="POS"):
        conjugation = "mi̠"
        if voice == "ACT":
            if type == "POS":
                #return self.conjugate_active(verb, conjugation, conjugation, with_replacement=False)
                return self.get_base_conjugation(verb, tense="IMP") + "mi̠"
            else:
                inf = self.get_base_conjugation(verb, voice="ACT", tense="INF")
                return remove_last_accent(inf)
        else:
            if type == "POS":
                if self.get_verb(verb)["verb_type"] == "t.n.i":
                    return self.conjugate_active(verb, conjugation, conjugation, with_replacement=False)
                return self.conjugate_middle(verb, "r" + conjugation)
            else:
                return self.conjugate_middle(verb, "nu̠k")

    def get_est_conjugation(self, verb, type="POS", mode="NONE", tense="REM", voice="ACT", aspect="NONE", absnum="NONE", person="NONE"):
        #REF: Book Grammatica
        if type == "NEG":
            return "ku̠"
        elif tense == "PRF_REC":
            return "tchá"
        elif tense == "PRF_REM":
            return "bák"
        else:
            return "tso'"

    def get_conjugation(self, verb, type="POS", mode="NONE", tense="REM", voice="ACT", aspect="NONE", absnum="NONE", person="NONE"):
        if verb in ["tso'", "tso", "ku̠"]:
            return self.get_est_conjugation(verb, type=type, mode=mode, tense=tense, voice=voice, aspect=aspect, absnum=absnum, person=person)
        
        conjugation = verb
        if mode == "DES":
            conjugation =  self.get_mode_des(verb)
        elif mode == "IMP":
            conjugation = self.get_mode_imp(verb, type=type, voice=voice)
        elif mode == "EXH":
            conjugation = self.get_mode_exh(verb)
        elif mode == "ADVERS":
            conjugation = self.get_mode_advers(verb)
        elif mode == "POT":
            conjugation = self.get_mode_pot(verb, type=type)
        elif tense == "IPFV_REC":
            suffix = self.active_suffix(verb) if voice == "ACT" else self.middle_suffix(verb)
            rec =  self.get_base_conjugation(verb, voice=voice, tense="IMP") + suffix
            if type == "NEG" and not rec.endswith("àr"):
                conjugation = remove_last_accent(rec)
            else:
                conjugation = rec
        elif tense == "PRF_REC":
            if type == "NEG":
                conjugation = self.conjugate_middle(verb, "ne̠") + self.middle_suffix(verb)
            elif voice == "ACT":
                conjugation = self.get_base_conjugation(verb, tense="REC") + self.middle_suffix(verb)
            else:
                conjugation = self.conjugate_middle(verb, "na̠") + self.middle_suffix(verb)
        elif tense == "PRF_PROG" or tense == "IPFV_PROG":
            suffix = "rë" if verb.endswith("rë") else ""
            conjugation = self.get_base_conjugation(verb, tense="INF") + suffix
        elif tense == "PAS_PLU":
            conjugation = self.get_mode_pasplu(verb)
        elif tense == "FUT_CER":
            conjugation = self.get_mode_futcer(verb, voice=voice, type=type)
        elif tense == "IPFV_HAB":
            conjugation = self.get_mode_hab(verb, voice=voice, type=type)
        elif tense == "FUT_POT":
            conjugation = self.get_mode_futpot(verb, voice=voice, type=type)
        elif type == "NEG" or voice == "MID":
            #conjugation = self.conjugate_middle(verb, "ne̠") + self.middle_suffix(verb)
            conjugation = self.get_base_conjugation(verb, voice="MID", tense="REM") + self.middle_suffix(verb)
        #elif voice == "MID" and tense == "REM":
        #    return self.get_base_conjugation(verb, voice="MID", tense="REM") + self.#middle_suffix(verb)
        #elif voice == "MID":
        #    assert False, f"MID mode not implemented TENSE:{tense}, TYPE:{type}, VOICE:{voice}, ASPECT:{aspect}, ABSNUM:{absnum}, PERSON:{person}"

        if aspect == "INC":
            conjugation += "mi̠"
        
        if absnum == "PL" and verb.endswith("stsa̠"):
            conjugation = replace_last(conjugation, "stsa̠", "ulur")

        return conjugation

    def get_all_verbs(self):
        return self.verb_dict.keys()

    def get_all_verb_data(self):
        return self.verb_dict
    
    def is_in_dict(self, word):
        if word in self.verb_dict:
            return True
        else:
            return False
