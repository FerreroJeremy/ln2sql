#!/usr/bin/python3
import os, sys, getopt
import unicodedata

from constants import color
from Database import Database
from LangConfig import LangConfig
from Parser import Parser
from Thesaurus import Thesaurus
from StopwordFilter import StopwordFilter


class ln2sql:
    def __init__(self, database_path, language_path, input_sentence, json_output_path, thesaurus_path, stopwords_path):

        database = Database()
        stopwordsFilter = None

        if thesaurus_path is not None:
            thesaurus = Thesaurus()
            thesaurus.load(thesaurus_path)
            database.set_thesaurus(thesaurus)

        if stopwords_path is not None:
            stopwordsFilter = StopwordFilter()
            stopwordsFilter.load(stopwords_path)
        
        database.load(database_path)
        #database.print_me()

        config = LangConfig()
        config.load(language_path)

        parser = Parser(database, config)

        queries = parser.parse_sentence(input_sentence, stopwordsFilter)

        if json_output_path is not None:
            self.remove_json(json_output_path)
            for query in queries:
                query.print_json(json_output_path)

        for query in queries:
            print(query)

    def remove_json(self, filename="output.json"):
        if os.path.exists(filename):
            os.remove(filename)

def print_help_message():
    print('\n')
    print('Usage:')
    print('\tpython ln2sql.py -d <path> -l <path> -i <input-sentence> [-j <path>] [-t <path>] [-s <path>]')
    print('Parameters:')
    print('\t-h\t\t\tprint this help message')
    print('\t-d <path>\t\tpath to SQL dump file')
    print('\t-l <path>\t\tpath to language configuration file')
    print('\t-i <input-sentence>\tinput sentence to parse')
    print('\t-j <path>\t\tpath to JSON output file')
    print('\t-t <path>\t\tpath to thesaurus file')
    print('\t-s <path>\t\tpath to stopwords file')
    print('\n')

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"d:l:i:j:t:s:")
        database_path = None
        input_sentence = None
        language_path = None
        thesaurus_path = None
        json_output_path = None
        stopwords_path = None

        for i in range(0, len(opts)):
            if opts[i][0] == "-d":
                database_path = opts[i][1]
            elif opts[i][0] == "-l":
                language_path = opts[i][1]
            elif opts[i][0] == "-i":
                input_sentence = opts[i][1]
            elif opts[i][0] == "-j":
                json_output_path = opts[i][1]
            elif opts[i][0] == "-t":
                thesaurus_path = opts[i][1]
            elif opts[i][0] == "-s":
                stopwords_path = opts[i][1]
            else:
                print_help_message()
                sys.exit()

        if (database_path is None) or (input_sentence is None) or (language_path is None):
            print_help_message()
            sys.exit()
        else:
            if thesaurus_path is not None:
                thesaurus_path = str(thesaurus_path)
            if stopwords_path is not None:
                stopwords_path = str(stopwords_path)
            if json_output_path is not None:
                json_output_path = str(json_output_path)

        ln2sql(str(database_path), str(language_path), str(input_sentence), json_output_path, thesaurus_path, stopwords_path)

    except getopt.GetoptError:
        print_help_message()
        sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])