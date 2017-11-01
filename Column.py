# -*- coding: utf-8 -*

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

class Column:
    name = ''
    type = ''
    primary = False
    foreign = False
    
    def __init__(self, name=None, type=None):
        if name is None:
            self.name = ''
        else:
            self.name = name

        if type is None:
            self.type = ''
        else:
            self.type = type

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type

    def is_primary(self):
        return self.primary

    def set_as_primary(self):
        self.primary = True

    def is_foreign(self):
        return self.foreign

    def set_as_foreign(self, references):
        self.foreign = references