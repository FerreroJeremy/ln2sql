# -*- coding: utf-8 -*

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import unicodedata

class Thesaurus:
    
    def __init__(self):
        self.dictionnary = {}
    
    def add_entry(self, word, synonyms):
        self.dictionnary[word] = synonyms
    
    def add_synonym_of_a_word(self, word, synonym):
        if word in self.dictionnary:
            self.dictionnary[word].append(synonym)
        else:
            self.dictionnary[word] = synonym
    
    def get_synonyms_of_a_word(self, word):
        if word in self.dictionnary.keys():
            return self.dictionnary[word]

    def remove_accents(self, string):
        nkfd_form = unicodedata.normalize('NFKD', unicode(string))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def load(self, path):
        with open(path) as f:
            content = f.readlines()
            # we jump content[0] because it is the encoding-type line : useless to parse
            for line_id in range(1,len(content)):
                if '(' not in content[line_id]:
                    line = content[line_id].split("|")
                    word = self.remove_accents(line[0])
                    synonyms = self.remove_accents(content[line_id + 1]).split("|")
                    synonyms.pop(0)
                    self.add_synonym_of_a_word(word, synonyms)

    def print_me(self):
        for keys,values in self.dictionnary.items():
            print(keys)
            print(values)
