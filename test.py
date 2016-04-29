#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

from Database import Database
from Thesaurus import Thesaurus
from Grammar import Grammar
from StopwordFilter import StopwordFilter

if __name__ == '__main__':
    #database = Database()
    #database.load(sys.argv[1])
    #database.print_me()

    #grammar = Grammar()
    #grammar.set_database(database)
    #grammar.parse_sentence(sys.argv[2])

    #thesaurus = Thesaurus()
    #thesaurus.load(sys.argv[3])
    #print(thesaurus.get_synonyms_of_a_word('eleve'))

    swf = StopwordFilter()
    swf.load('french')
    print swf.filter(sys.argv[1].split(' '))