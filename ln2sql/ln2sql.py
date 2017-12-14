#!/usr/bin/python3
import argparse
import os

from .database import Database
from .langConfig import LangConfig
from .parser import Parser
from .stopwordFilter import StopwordFilter
from .thesaurus import Thesaurus


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
        # database.print_me()

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
