# -*- coding: utf-8 -*

import sys
import unicodedata


class Column:
    name = ''
    type = []
    equivalences = []
    primary = False
    foreign = False
    
    def __init__(self, name=None, type=None, equivalences=None):
        if name is None:
            self.name = ''
        else:
            self.name = name

        if type is None:
            self.type = []
        else:
            self.type = type
 
        if equivalences is None:
            self.equivalences = []
        else:
            self.equivalences = equivalences

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type

    def add_type(self, type):
        self.type.append(type)

    def get_equivalences(self):
        return self.equivalences

    def set_equivalences(self, equivalences):
        self.equivalences = equivalences

    def add_equivalence(self, equivalence):
        self.equivalences.append(equivalence)

    def is_equivalent(self, word):
        if word in self.equivalences:
            return true
        else:
            return false

    def is_primary(self):
        return self.primary

    def set_as_primary(self):
        self.primary = True

    def is_foreign(self):
        return self.foreign

    def set_as_foreign(self, references):
        self.foreign = references