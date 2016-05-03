# -*- coding: utf-8 -*

import os

from Database import Database
from Parser import Parser
from Generator import Generator
from Thesaurus import Thesaurus
from StopwordFilter import StopwordFilter

class ln2sql:
    def __init__(self, database_name, input_sentence, language, thesaurus_use=None, json_output_path=None):
        database = Database()
        database.load(database_name)
        #database.print_me()

        try:
            parser = Parser()
            parser.set_database(database)
            parser.set_language(language)

            if thesaurus_use is not None:
                thesaurus = Thesaurus()
                thesaurus.load('./thesaurus/th_' + language + '.dat')
                parser.set_thesaurus(thesaurus)

            queries = parser.parse_sentence(input_sentence)

            if json_output_path is not None:
                self.remove_json(json_output_path)
                for query in queries:
                    query.print_me(json_output_path)
                    
        except Exception, e:
            print e

    def remove_json(self, filename="output.json"):
        if os.path.exists(filename):
            os.remove(filename)