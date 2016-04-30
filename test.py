#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

from Database import Database
from Thesaurus import Thesaurus
from Grammar import Grammar
from StopwordFilter import StopwordFilter

if __name__ == '__main__':
    database = Database()
    database.load(sys.argv[1])
    #database.print_me()

    try:
        grammar = Grammar()
        grammar.set_database(database)
        grammar.parse_sentence(sys.argv[2])
    except Exception, e:
        print e