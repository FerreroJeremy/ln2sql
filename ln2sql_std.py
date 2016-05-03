#!/usr/bin/python
# -*- coding: utf-8 -*

import sys, getopt

from ln2sql import ln2sql

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
        database_name = None
        input_sentence = None
        language = None
        thesaurus_usage = None
        json_output_path = None

        for i in range(0, len(opts)):
            if opts[i][0] == "-d":
                database_name = opts[i][1]
            elif opts[i][0] == "-l":
                language = opts[i][1]
            elif opts[i][0] == "-i":
                input_sentence = opts[i][1]
            elif opts[i][0] == "-j":
                json_output_path = opts[i][1]
            elif opts[i][0] == "-t":
                thesaurus_usage = True
            else:
                print_help_message()
                sys.exit()

        if (database_name is None) or (input_sentence is None) or (language is None):
            print_help_message()
            sys.exit()
        else:
            if thesaurus_usage is not None:
                thesaurus_usage = True
            if json_output_path is not None:
                json_output_path = str(json_output_path)

            ln2sql(str(database_name), str(input_sentence), str(language), thesaurus_usage, json_output_path)

    except getopt.GetoptError:
        print_help_message()
        sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
