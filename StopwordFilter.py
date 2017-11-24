# -*- coding: utf-8 -*

import re
import sys
import unicodedata


class StopwordFilter:
    
    def __init__(self):
        self.list = []
    
    def add_stopword(self, word):
        self.list.append(word)

    def get_stopword_list(self):
        return self.list
    
    def filter(self, sentence):
        tmp_sentence = ""
        words = re.findall(r"[\w]+", self.remove_accents(sentence))
        for word in words:
            word = self.remove_accents(word).lower()
            if word not in self.list:
                tmp_sentence += word + " "
        return tmp_sentence.strip()

    def remove_accents(self, string):
        nkfd_form = unicodedata.normalize('NFKD', str(string))
        return "".join([c for c in nkfd_form if not unicodedata.combining(c)])

    def load(self, path):
        with open(path) as f:
            lines = f.read().split('\n')
            for word in lines:
                stopword = self.remove_accents(word).lower()
                self.add_stopword(stopword)
