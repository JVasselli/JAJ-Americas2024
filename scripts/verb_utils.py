def replace_last(str, before, after):
    parts = str.split(before)
    if len(parts) < 2:
        return str
    final = before.join(parts[:-1]) + after + parts[-1]
    return final

def find_last_vowel(verb):
    for i in range(len(verb) - 1, -1, -1):
        if verb[i] in ["a", "i", "o", "u", "e", "ö", "ë", "ù", "ú", "è", "é", "ò", "ó", "ì", "í"]:
            return (i, i)
        elif verb[i] in ["̀", "́"]:
            return (i - 1, i)
    return (0, 0)

def add_accent_to_last_vowel(verb, accent):
    start, _ = find_last_vowel(verb)
    vowel = verb[start]
    if vowel == "i" and accent == "/":
        return replace_last(verb, "i", "í")
    if vowel == "i" and accent == "\\":
        return replace_last(verb, "i", "ì")
    if vowel == "o" and accent == "/":
        return replace_last(verb, "o", "ó")
    if vowel == "o" and accent == "\\":
        return replace_last(verb, "o", "ò")
    if vowel == "u" and accent == "/":
        return replace_last(verb, "u", "ú")
    if vowel == "u" and accent == "\\":
        return replace_last(verb, "u", "ù")
    if vowel == "e" and accent == "/":
        return replace_last(verb, "e", "é")
    if vowel == "e" and accent == "\\":
        return replace_last(verb, "e", "è")
    if vowel == "a" and accent == "/":
        return replace_last(verb, "a", "á")
    if vowel == "a" and accent == "\\":
        return replace_last(verb, "a", "à")
    if vowel == "ö" and accent == "/":
        return replace_last(verb, "ö", "ö́")
    if vowel == "ö" and accent == "\\":
        return replace_last(verb, "ö", "ö̀")
    if vowel == "ë" and accent == "/":
        return replace_last(verb, "ë", "ë́")
    if vowel == "ë" and accent == "\\":
        return replace_last(verb, "ë", "ë̀")
    return verb

def remove_last_accent(verb):
    for char in reversed(verb):
        if char in ["a", "i", "o", "u", "e", "ö", "ë"]:
            return verb
        if char == "̀":
            return replace_last(verb, "̀", "")
        if char == "́":
            return replace_last(verb, "́", "")
        if char == "ì":
            return replace_last(verb, "ì", "i")
        if char == "ò":
            return replace_last(verb, "ò", "o")
        if char == "ù":
            return replace_last(verb, "ù", "u") 
        if char == "è":
            return replace_last(verb, "è", "e")
        if char == "á":
            return replace_last(verb, "á", "a")
        if char == "à":
            return replace_last(verb, "à", "a")
        if char == "í":
            return replace_last(verb, "í", "i")
        if char == "ó":
            return replace_last(verb, "ó", "o")
        if char == "ú":
            return replace_last(verb, "ú", "u")
        if char == "é":
            return replace_last(verb, "é", "e")
        
    return verb


