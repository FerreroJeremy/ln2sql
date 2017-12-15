import os
import unicodedata


class Thesaurus:
    def __init__(self):
        self.dictionary = {}

    def add_entry(self, word, synonyms):
        self.dictionary[word] = synonyms

    def add_synonym_to_a_word(self, word, synonym):
        self.dictionary[word].append(synonym)

    def add_synonyms_to_a_word(self, word, synonyms):
        if word in self.dictionary:
            self.dictionary[word] += synonyms
        else:
            self.dictionary[word] = synonyms

    def get_synonyms_of_a_word(self, word):
        if word in list(self.dictionary.keys()):
            return self.dictionary[word]

    def remove_accents(self, string):
        nkfd_form = unicodedata.normalize('NFKD', str(string))
        return "".join([c for c in nkfd_form if not unicodedata.combining(c)])

    @staticmethod
    def _generate_path(path):
        cwd = os.path.dirname(__file__)
        filename = os.path.join(cwd, path)
        return filename

    def load(self, path):
        with open(self._generate_path(path)) as f:
            content = f.readlines()
            # we jump content[0] because it is the encoding-type line : useless to parse
            for line_id in range(1, len(content)):
                if '(' not in content[line_id]:
                    line = content[line_id].split("|")
                    word = self.remove_accents(line[0])
                    synonyms = self.remove_accents(content[line_id + 1]).split("|")
                    synonyms.pop(0)
                    self.add_synonyms_to_a_word(word, synonyms)

    def print_me(self):
        for keys, values in list(self.dictionary.items()):
            print(keys)
            print(values)
