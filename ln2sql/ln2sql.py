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
            json_output_path=None,
            thesaurus_path=None,
            stopwords_path=None,
    ):

        database = Database()
        self.stopwordsFilter = None

        if thesaurus_path:
            thesaurus = Thesaurus()
            thesaurus.load(thesaurus_path)
            database.set_thesaurus(thesaurus)

        if stopwords_path:
            self.stopwordsFilter = StopwordFilter()
            self.stopwordsFilter.load(stopwords_path)

        database.load(database_path)
        # database.print_me()

        config = LangConfig()
        config.load(language_path)

        self.parser = Parser(database, config)
        self.json_output_path = json_output_path

    def get_query(self, input_sentence):
        queries = self.parser.parse_sentence(input_sentence, self.stopwordsFilter)

        if self.json_output_path:
            self.remove_json(json_output_path)
            for query in queries:
                query.print_json(self.json_output_path)

        full_query = ''

        for query in queries:
            full_query += str(query)
            print(query)

        return full_query

    def remove_json(self, filename="output.json"):
        if os.path.exists(filename):
            os.remove(filename)
