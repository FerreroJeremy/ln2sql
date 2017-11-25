#!/usr/bin/python3
import os, sys
import unicodedata

from .database import Database
from .langConfig import LangConfig
from .parser import Parser
from .thesaurus import Thesaurus
from .stopwordFilter import StopwordFilter


class Ln2sql:
    def __init__(
        self,
        database_path,
        language_path,
        input_sentence,
        json_output_path=None,
        thesaurus_path=None,
        stopwords_path=None,
    ):

        database = Database()
        stopwordsFilter = None

        if thesaurus_path:
            thesaurus = Thesaurus()
            thesaurus.load(thesaurus_path)
            database.set_thesaurus(thesaurus)

        if stopwords_path:
            stopwordsFilter = StopwordFilter()
            stopwordsFilter.load(stopwords_path)

        database.load(database_path)
        #database.print_me()

        config = LangConfig()
        config.load(language_path)

        parser = Parser(database, config)

        queries = parser.parse_sentence(input_sentence, stopwordsFilter)

        if json_output_path:
            self.remove_json(json_output_path)
            for query in queries:
                query.print_json(json_output_path)

        self.full_query = ''
        for query in queries:
            self.full_query += str(query)
            print(query)

    def get_query(self):
        return self.full_query

    def remove_json(self, filename="output.json"):
        if os.path.exists(filename):
            os.remove(filename)


def main():
    arg_parser = argparse.ArgumentParser(description='A Utility to convert Natural Language to SQL query')
    arg_parser.add_argument('-d', '--database', help='Path to SQL dump file', required=True)
    arg_parser.add_argument('-l', '--language', help='Path to language configuration file', required=True)
    arg_parser.add_argument('-i', '--sentence', help='Input sentence to parse', required=True)
    arg_parser.add_argument('-j', '--json_output', help='path to JSON output file', default=None)
    arg_parser.add_argument('-t', '--thesaurus', help='path to thesaurus file', default=None)
    arg_parser.add_argument('-s', '--stopwords', help='path to stopwords file', default=None)

    args = arg_parser.parse_args()

    Ln2sql(
        database_path=args.database,
        language_path=args.language,
        input_sentence=args.sentence,
        json_output_path=args.json_output,
        thesaurus_path=args.thesaurus,
        stopwords_path=args.stopwords,
    )

if __name__ == '__main__':
    main()
