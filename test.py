#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

from Database import Database
from Thesaurus import Thesaurus

if __name__ == '__main__':
    database = Database()
    database.load(sys.argv[1])
    #database.print_me()

    thesaurus = Thesaurus()
    thesaurus.load(sys.argv[2])
    #thesaurus.print_me()
    print(thesaurus.get_synonyms_of_a_word('élève'))
    print(thesaurus.get_synonyms_of_a_word('eleve'))