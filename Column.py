# -*- coding: utf-8 -*

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

class Column:
    name = ''
    type = ''
    is_primary = False
    
    def __init__(self, name=None, type=None, is_primary=None):
        if name is None:
            self.name = ''
        else:
            self.name = name
        if type is None:
            self.type = ''
        else:
            self.type = type
        if is_primary is None:
            self.is_primary = False
        else:
            self.is_primary = is_primary

    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type

    def is_primary(self):
        return self.is_primary