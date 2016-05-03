#!/usr/bin/python
# -*- coding: utf-8 -*

import sys, os, getopt

from Database import Database
from Thesaurus import Thesaurus
from Grammar import Grammar
from StopwordFilter import StopwordFilter

from Query import *

def remove_json(filename="output.json"):
    if os.path.exists(filename):
        os.remove(filename)

def print_help_message():
    print 'usage: ./ln2sql.py -d <path> -l <language> -i <input-sentence> [-t] [-j <path>]'
    print '-h\t\t\tprint this help message'
    print '-d <path>\t\tpath to sql dump file'
    print '-l <language>\t\tlanguage of the input sentence'
    print '-i <input-sentence>\tinput sentence to parse'
    print '-j <path>\t\tpath to JSON output file'
    print '-t\t\t\tuse thesaurus'

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"d:l:i:tj:")
        database_name = ''
        input_sentence = ''
        language = ''
        thesaurus_usage = False
        path_json_file = ''

        for i in range(0, len(opts)):
            if opts[i][0] == "-d":
                database_name = opts[i][1]
            elif opts[i][0] == "-l":
                language = opts[i][1]
            elif opts[i][0] == "-i":
                input_sentence = opts[i][1]
            elif opts[i][0] == "-j":
                path_json_file = opts[i][1]
            elif opts[i][0] == "-t":
                thesaurus_usage = True
            else:
                print_help_message()
                sys.exit()

        if database_name == '' or input_sentence == '' or language == '':
            print_help_message()
            sys.exit()
        else:
            database = Database()
            database.load(str(database_name))
            #database.print_me()

            try:
                grammar = Grammar()
                grammar.set_database(database)
                grammar.set_language(language)
                queries = grammar.parse_sentence(str(input_sentence))
                if path_json_file != '':
                    remove_json(str(path_json_file))
                    for query in queries:
                        query.print_me(str(path_json_file))
            except Exception, e:
                print e

    except getopt.GetoptError:
        print_help_message()
        sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
