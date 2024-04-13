import pandas as pd


class Example:
    def __init__(self, source, target, change):
        self.source = source
        self.target = target
        self.change = change
        self.change_components = change.split(", ")

    def has_component(self, component):
        return component in self.change_components

    def dict(self):
        return {"source": self.source, "target": self.target, "change": self.change}

    def __str__(self):
        return f"{self.source} -> {self.target} Change: {self.change}"

    def __hash__(self):
        return hash(self.source + self.change)

    def __eq__(self, other):
        return self.source == other.source and self.change == other.change


class ExamplesDatabase:
    def __init__(self, examples_file):
        self.examples_df = pd.read_csv(examples_file, sep="\t")

        # Create a dictionary of examples
        # key: change
        # value: Example
        self.examples = []
        self.change_index = {}
        for _, row in self.examples_df.iterrows():
            new_example = Example(row["Source"], row["Target"], row["Change"])
            self.examples.append(new_example)
            if row["Change"] not in self.change_index:
                self.change_index[row["Change"]] = []
            self.change_index[row["Change"]].append(new_example)

    def look_for_superset_changes(self, change):
        superset_changes = []
        for key in self.change_index:
            if change in key:
                superset_changes.append((key, len(key.split(","))))
        if superset_changes != []:
            superset_changes.sort(key=lambda x: x[1])
            examples = []
            for key, _ in superset_changes:
                examples += self.change_index[key]
            return examples[:15]
        return []

    def look_for_subset_changes(self, change):
        examples = []
        components = change.split(", ")
        for i in range(len(components) - 1, -1, -1):
            combined = ", ".join(components[:i])
            if not combined in self.change_index:
                continue
            examples += self.change_index[combined]
        for i in range(0, len(components)):
            combined = ", ".join(components[i:])
            if not combined in self.change_index:
                continue
            examples += self.change_index[combined]
        return examples

    def retrieve_from_change(self, change, exact_match=True):
        if change in self.change_index:
            return self.change_index[change]
        if exact_match:
            return []
        else:
            examples = self.look_for_superset_changes(change)
            if examples == []:
                examples = self.look_for_subset_changes(change)
            return examples

    def get_best_examples_for_changes(self, changes, source, k=1):
        return [(c, 0) for c in self.retrieve_from_change(changes)]
