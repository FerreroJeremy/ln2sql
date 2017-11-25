# -*- coding: utf-8 -*

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

from Column import Column

class Table:
    name = ''
    columns = []
    equivalences = []
    
    def __init__(self, name=None, columns=None, equivalences=None):
        if name is None:
            self.name = ''
        else:
            self.name = name

        if columns is None:
            self.columns = []
        else:
            self.columns = columns

        if equivalences is None:
            self.equivalences = []
        else:
            self.equivalences = equivalences
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    def get_number_of_columns(self):
        return len(self.columns)
    
    def get_columns(self):
        return self.columns

    def get_column_by_name(self, column_name):
        for column in self.columns:
            if column.get_name() == column_name:
                return column

    def add_column(self, column_name, column_type, column_equivalences):
        self.columns.append(Column(column_name, column_type, column_equivalences))

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

    def get_primary_keys(self):
        primary_keys = []
        for column in self.columns:
            if column.is_primary():
                primary_keys.append(column)
        return primary_keys

    def get_primary_key_names(self):
        primary_keys = []
        for column in self.columns:
            if column.is_primary():
                primary_keys.append(column.get_name())
        return primary_keys

    def add_primary_key(self, primary_key_column):
        for column in self.columns:
            if column.get_name() == primary_key_column:
                column.set_as_primary()

    def get_foreign_keys(self):
        foreign_keys = []
        for column in self.columns:
            if column.is_foreign():
                foreign_keys.append(column)
        return foreign_keys

    def get_foreign_key_names(self):
        foreign_keys = []
        for column in self.columns:
            if column.is_foreign():
                foreign_keys.append(column.get_name())
        return foreign_keys

    def add_foreign_key(self, column_name, foreign_table, foreign_column):
        for column in self.columns:
            if column.get_name() == column_name:
                column.set_as_foreign({'foreign_table':foreign_table,'foreign_column':foreign_column})