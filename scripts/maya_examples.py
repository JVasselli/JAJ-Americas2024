from examples import ExamplesDatabase
from maya_util import similarity_score

class MayaExamplesDatabase(ExamplesDatabase):
    def __init__(self):
        super(MayaExamplesDatabase, self).__init__("../ref/maya-examples.tsv")
        self.sources = {}
        for example in self.examples:
            source = example.source
            if source not in self.sources:
                self.sources[source] = []
            self.sources[source].append(example)

    def find_most_similar_sources(self, source_sentence, k=1):
        closest_sources = []
        for source in self.sources:
            similarity = similarity_score(source_sentence, source)
            closest_sources.append((source, similarity))
        return sorted(closest_sources, key=lambda x: x[1], reverse=True)[:k]
    
    def get_examples_for_source(self, source, change_filter=None):
        if source not in self.sources:
            return []
        if not change_filter:
            return self.sources[source]
        return [item for item in self.sources[source] if change_filter in item.change]
    
    def get_examples_for_change(self, change, strict=True):
        if strict:
            return [item for item in self.examples if change == item.change]
        return [item for item in self.examples if change in item.change]
    
    def get_best_examples_for_change(self, change, source, k=1):
        #Look at only the examples that contain the change, but sort by closest source
        examples = self.get_examples_for_change(change)
        if len(examples) == 0:
            examples = self.get_examples_for_change(change, strict=False)
            
        sources = []
        for example in examples:
            sources.append((example, similarity_score(source, example.source)))
        return sorted(sources, key=lambda x: x[1], reverse=True)[:k]

    def get_best_examples_for_changes(self, changes, source, k=1):
        change_components = changes.split(", ")
        examples = []
        for c in change_components:
            examples += self.get_best_examples_for_change(c, source, k*2)
        #deduplicate
        examples = list(set(examples))
        #resort
        examples = sorted(examples, key=lambda x: x[1], reverse=True)
        # need to make sure that all components are represented
        first_indicies = []
        for c in change_components:
            for i, e in enumerate(examples):
                if c in e[0].change:
                    first_indicies.append(i)
                    break
        one_of_each = list(set([examples[i] for i in first_indicies] + examples[:k]))
        return one_of_each

if __name__=="__main__":
    examples_db = MayaExamplesDatabase()
    print(examples_db.get_best_examples_for_change("SUBTYPE:INT", "Ma' ta jutaj a najili'", 5))
