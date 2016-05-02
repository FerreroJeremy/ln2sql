#!/usr/bin/python
# -*- coding: utf-8 -*

import sys
import os

from Database import Database
from Thesaurus import Thesaurus
from Grammar import Grammar
from StopwordFilter import StopwordFilter

from Query import *

def remove_json(filename="output.json"):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == '__main__':

    database = Database()
    database.load(str(sys.argv[1]))
    database.print_me()

    try:
        grammar = Grammar()
        grammar.set_database(database)
        queries = grammar.parse_sentence(str(sys.argv[2]))
        remove_json()
        for query in queries:
            query.print_me()
    except Exception, e:
        print e

