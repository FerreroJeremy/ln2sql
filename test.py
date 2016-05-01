#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

from Database import Database
from Thesaurus import Thesaurus
from Grammar import Grammar
from StopwordFilter import StopwordFilter

from Query import *

if __name__ == '__main__':
    '''
    database = Database()
    database.load(sys.argv[1])
    database.print_me()

    try:
        grammar = Grammar()
        grammar.set_database(database)
        grammar.parse_sentence(sys.argv[2])
    except Exception, e:
        print e
    '''
    query = Query(Select(True, ['nom', 'prenom', 'age']), From('eleve'), Join(['professeur', 'classe']))
    condition1 = Condition('nom', '==', 'Nemmar')
    condition2 = Condition('prenom', '==', 'Jean')
    condition3 = Condition('age', '>=', '16')
    where = Where(condition1)
    where.add_condition('and', condition2)
    where.add_condition('or', condition3)
    query.set_where(where)
    query.set_group_by(GroupBy(['nom', 'prenom']))
    query.set_order_by(OrderBy('nom', 'desc'))
    query.print_me()