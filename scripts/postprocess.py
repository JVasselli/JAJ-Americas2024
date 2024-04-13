import argparse
import json
import re
import pandas as pd

try:
    import enchant
    eng_dict = enchant.Dict("en_US")
except:
    pass

def parse_args():
    parser = argparse.ArgumentParser(description="Find examples of cases in a file")
    parser.add_argument(
        "--data",
        help="The folder containing the data",
        default="../data/",
    )
    parser.add_argument("--language", help="The language to run the script on")
    parser.add_argument("--output", help="The folder to write the output to")
    parser.add_argument("--debug", help="Run in debug mode", action="store_true")
    return parser.parse_args()

def is_ascii(word):
    try:
        return word.encode('ascii')
    except:
        return False

def language_guess_from_answer(string):
    language_guess = []
    for token in string.split():
        if not is_ascii(token):
            language_guess.append(1)
        elif token.endswith("'"):
            language_guess.append(1)
        elif "aa" in token or "ii" in token or "a'a" in token or "e'e" in token:
            language_guess.append(1)
        elif eng_dict and not eng_dict.check(token):
            language_guess.append(1)
        else:
            language_guess.append(0)
    
    #if there are near consecutive strings of 1s broken by a single 0, mark the 0 as 1
    for i in range(1, len(language_guess)-1):
        if language_guess[i-1] == 1 and language_guess[i] == 0 and language_guess[i+1] == 1:
            language_guess[i] = 1
    return language_guess


def extract_non_english(string):
    string = string.replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace(":", "").replace(";", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("\"", "")
    language_guess = language_guess_from_answer(string)
    string = string.split()

    #print(list(zip(string, language_guess)))

    matches = []
    curr_string = ""
    for lang, tok in zip(language_guess, string):
        if lang == 1:
            curr_string += tok + " "
        else:
            if curr_string != "":
                matches.append(curr_string.strip())
            curr_string = ""
    if curr_string != "":
        matches.append(curr_string.strip())

    return matches

def prediction_from_answer(string, change="", original=""):
    re_change = re.compile(r"([A-Z]+:[A-Z_]+(,\s)?)+")
    re_quotes = re.compile(r"\"(.*?)\"")

    for line in string.split("\n"):
        if line.strip().endswith(":"):
            continue
        if line.strip() == "":
            continue

        line = line.replace(".", "")

        if "->" in line:
            line = line.split("->")[-1].strip()
        elif "→" in line:
            line = line.split("→")[-1].strip()
        elif "Answer: " in line or "Prediction: " in line and "\"" not in line:
            line = line.split(": ")[-1].strip()
            if "(" in line:
                line = line.split("(")[0].strip()
            return line
        elif ": " in line:
            line = line.split(": ")[-1].strip()
        
        if "(" in line:
            line = line.split("(")[0].strip()

        matches = list(re_quotes.findall(line))
        if len(matches) == 0:
            language_guess = language_guess_from_answer(line)
            #if the number of 0s is low, return line
            if language_guess.count(0) < 3:
                line = line[0].upper() + line[1:]
                return line
            
            matches = extract_non_english(line)

        if len(matches) == 0:
            continue
        elif len(matches) == 1:
            prediction = matches[0].strip()
        elif len(matches) > 1:
            #print(matches)
            longest = 0
            for match in matches:
                if match.strip() == original.strip():
                    #print("found original")
                    continue
                #check if match matches the re_change
                if re_change.match(match):
                    #print("found change")
                    continue
                else:
                    print("testing \"{}\" == \"{}\"".format(match.strip(), original.strip()))

                if len(match.split()) > longest:
                    longest = len(match)
                    prediction = match

        if "(" in prediction:
            prediction = prediction.split("(")[0].strip()
        
        #make sure the first letter is capitalized
        prediction = prediction[0].upper() + prediction[1:]
        return prediction


def predictions_from_results(args):
    input_file = args.data + f"{args.language}-dev.tsv"
    if args.language == "bribri":
        input_file = args.data + "bribri-dev-plus.tsv"
        
    cases_df = pd.read_csv(input_file, sep="\t")
    if args.debug:
        cases_df = cases_df[:10]

    cases = []
    for _, row in cases_df.iterrows():
        cases.append(
            {
                "id": row["ID"],
                "source": row["Source"],
                "change": row["Change"],
            }
        )

    results = json.load(open(f"{args.output}{args.language}-output.json", "r"))

    assert len(cases) == len(results)

    predictions = []
    # Things happen here!!
    for c, r in zip(cases, results):
        prediction = prediction_from_answer(r, change=c["change"], original=c["source"])
        
        print(c["id"])
        print(c["source"], "->", prediction)
        print(r)
        print()
        #input()

        assert prediction is not None
        predictions.append(prediction)

    cases_df["Predicted Target"] = predictions

    # Find examples of the cases
    output_file = args.output + f"{args.language}-dev-prediction.tsv"
    cases_df.to_csv(output_file, sep="\t", index=False)


def main():
    args = parse_args()
    predictions_from_results(args)


if __name__ == "__main__":
    main()
