import csv
import json
from maya_examples import MayaExamplesDatabase
from maya_util import pos_tag_maya, convert_changes_maya, hint_from_change_maya
from bribri_verb_util import BribriVerbDatabase
from bribri_util import pos_tag_bribri, convert_changes_bribri, hint_from_change_bribri, verb_in_source
from examples import ExamplesDatabase
from generator import Generator
from postprocess import prediction_from_answer

from argparse import ArgumentParser
import os

from tqdm import tqdm

def parse_args():
    parser = ArgumentParser(description="Prompt a model with carefully chosen examples")
    parser.add_argument("--split", help="The split to use", default="dev")
    parser.add_argument("--model_name", help="The model to use")
    parser.add_argument("--debug", help="Run in debug mode", action="store_true")
    parser.add_argument(
        "--num_examples", help="Number of examples to use", type=int, default=5
    )
    parser.add_argument("--language", type=str)
    parser.add_argument("--output", type=str, default="../results/")
    return parser.parse_args()

def load_data(file):
    changes = []
    with open(file, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            changes.append(row)
    return changes

class SentenceChanger:
    def __init__(self, language, model):
        self.language = language
        if language == "maya":
            self.examples_db = MayaExamplesDatabase()
        elif language == "bribri":
            self.verb_db = BribriVerbDatabase()
            self.examples_db = ExamplesDatabase(f"../ref/{language}-examples.tsv")
        else:
            self.examples_db = ExamplesDatabase(f"../ref/{language}-examples.tsv")
        
        self.generator = Generator(model, show_progress=False)

    def pos_tag_string(self, string):
        if self.language == "maya":
            return pos_tag_maya(string)
        if self.language == "bribri":
            return pos_tag_bribri(string)
        
    def convert_changes(self, changes):
        if self.language == "maya":
            return convert_changes_maya(changes)
        if self.language == "bribri":
            return convert_changes_bribri(changes)
        
    def hint_from_change(self, change, source):
        if self.language == "maya":
            return hint_from_change_maya(change)
        if self.language == "bribri":
            hint = hint_from_change_bribri(change)
            if "PERSON" not in change:
                hint += self.verb_hint(source, change)
            return hint
        
    def verb_hint(self, source, change):
        verb_source = verb_in_source(source)
    
        if verb_source and self.verb_db.get_verb(verb_source):
            changes = {component.split(":")[0].lower().strip(): component.split(":")[1].strip() for component in change.split(",")}
            source_conjugation = self.verb_db.get_conjugation(verb_source, **changes)
            return f"The correct form of {verb_source} is likely {source_conjugation}\n"
        return ""

    def apply_changes_to_string(self, id, changes, string, num_examples):
        curr_string = string
        question_history = []
        result_history = []
        for change in self.convert_changes(changes):
            examples = self.examples_db.get_best_examples_for_changes(change, curr_string, k=num_examples)
            examples = [e[0] for e in examples]
            examples = [{
                "source": e.source,
                "change": e.change,
                "target": e.target,
                "tagged_source" : self.pos_tag_string(e.source),
                "tagged_target": self.pos_tag_string(e.target),
                "language": self.language
            } for e in examples]
            question = {
                "source": curr_string,
                "change": change,
                "hint": self.hint_from_change(change, curr_string),
                "tagged_source": self.pos_tag_string(string),
                "examples": examples
            }
            question_history.append(question)
            results = self.generator.prompt(
                [question],
                "../prompts/pos_tagged_prompt.txt",
                stop=["\n\n"]
            )
            result = {
                "ID": id,
                "Source": string,
                "Change": change,
                "system_output": results[0],
                }
            result_history.append(result)
            curr_string = prediction_from_answer(results[0], change=change, original=curr_string)

        return question_history, result_history, curr_string

if __name__ == "__main__": 
    args = parse_args()
    changer = SentenceChanger(args.language, args.model_name)

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    data = load_data(f"../data/{args.language}-{args.split}.tsv")

    if args.debug:
        data = data[:10]

    questions = []
    results = []
    predictions = []
    for item in tqdm(data):
        question, result, prediction = changer.apply_changes_to_string(
            item["ID"], item["Change"], item["Source"], args.num_examples)
        questions.append(question)
        results.append(result)
        predictions.append(prediction)

    with open(args.output + f"{args.language}-{args.split}-questions.json", "w") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

    with open(args.output + f"{args.language}-{args.split}-output.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    for i, item in enumerate(data):
        item["Predicted Target"] = predictions[i]
    
    #write out predictions to csv
    #ID	Source	Change	Target	Predicted Target
    with open(args.output + f"{args.language}-{args.split}-prediction.tsv", "w") as f:
        fieldnames = ["ID", "Source", "Change", "Target", "Predicted Target"]
        f.write("ID	Source	Change	Target	Predicted Target\n")
        for d in data:
            f.write("\t".join([d[field] for field in fieldnames]) + "\n")
