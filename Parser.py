# -*- coding: utf-8 -*

import re
import sys
import unicodedata
from Exception import ParsingException
from Query import *

reload(sys)
sys.setdefaultencoding("utf-8")

class Parser:
    database_object = None
    database_dico = None
    language = None
    thesaurus_object = None

    count_keywords = []
    junction_keywords = []
    disjunction_keywords = []

    french_count_keywords = ['combien', 'nombre']
    french_junction_keywords = ['et']
    french_disjunction_keywords = ['ou']

    english_count_keywords = ['how many', 'number']
    english_junction_keywords = ['and']
    english_disjunction_keywords = ['or']
    
    def __init__(self, language=None, database=None):
        if language is not None:
            self.language = language
        else:
            self.language = 'french'

        self.load_language_resources()

        if database is not None:
            self.database_object = database
            self.database_dico = self.database_object.get_tables_into_dictionnary()

    def load_language_resources(self):
        if self.language == 'french':
            self.count_keywords = self.french_count_keywords
            self.junction_keywords = self.french_junction_keywords
            self.disjunction_keywords = self.french_disjunction_keywords
        elif self.language == 'english':
            self.count_keywords = self.english_count_keywords
            self.junction_keywords = self.english_junction_keywords
            self.disjunction_keywords = self.english_disjunction_keywords
        else:
            raise ParsingException("No resource found!")

    def set_database(self, database):
        self.database_object = database
        self.database_dico = self.database_object.get_tables_into_dictionnary()

    def set_language(self, language):
        self.language = language
        self.load_language_resources()

    def set_thesaurus(self, thesaurus):
        self.thesaurus_object = thesaurus
    
    def remove_accents(self, string):
        nkfd_form = unicodedata.normalize('NFKD', unicode(string))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
    
    def parse_sentence(self, sentence):
        number_of_table = 0
        number_of_select_column = 0
        number_of_where_column = 0
        last_table_position = 0
        columns_of_select = []
        columns_of_where = []
        tables_of_from = []
        select_phrase = ''
        from_phrase = ''
        where_phrase = ''
        
        words = re.findall(r"[\w]+", self.remove_accents(sentence))

        for i in range(0, len(words)):
            if words[i] in self.database_dico:
                if number_of_table == 0:
                    select_phrase = words[:i]
                tables_of_from.append(words[i])
                number_of_table+=1
                last_table_position = i
            for table in self.database_dico:
                if words[i] in self.database_dico[table]:
                    if number_of_table == 0:
                        columns_of_select.append(words[i])
                        number_of_select_column+=1
                    else:
                        if number_of_where_column == 0:
                            from_phrase = words[len(select_phrase):last_table_position+1]
                        columns_of_where.append(words[i])
                        number_of_where_column+=1
                    break
                else:
                    if number_of_table != 0 and number_of_where_column == 0 and i == (len(words)-1):
                        from_phrase = words[len(select_phrase):]

        where_phrase = words[len(select_phrase) + len(from_phrase):]
        
        if (number_of_select_column + number_of_table + number_of_where_column) == 0:
            raise ParsingException("No keyword found in sentence!")
        
        select_object = self.parse_select(columns_of_select, select_phrase)
        queries = self.parse_from(tables_of_from, from_phrase, columns_of_select, columns_of_where)
        where_object = self.parse_where(number_of_where_column, where_phrase)

        for query in queries:
            query.set_select(select_object)
            query.set_where(where_object)
            query.set_group_by(GroupBy())
            query.set_order_by(OrderBy())

        return queries

    def parse_select(self, columns_of_select, phrase):
        select_object = Select()
        is_count_select_query = False
        number_of_select_column = len(columns_of_select)

        for count_keyword in self.count_keywords:
            if count_keyword in phrase:
                is_count_select_query = True

        if is_count_select_query:
            select_object.set_count_type(True)
        else:
            select_object.set_count_type(False)

        for column in columns_of_select:
            select_object.add_column(column)

        return select_object
    
    def parse_from(self, tables_of_from, phrase, columns_of_select, columns_of_where):
        if len(tables_of_from) == 0:
            raise ParsingException("No table name found in sentence!")

        real_tables_of_from =[]
        queries = []
        number_of_junction_words = 0
        number_of_disjunction_words = 0

        for word in phrase:
            if word in self.junction_keywords:
                number_of_junction_words += 1
            if word in self.disjunction_keywords:
                number_of_disjunction_words += 1

        if (number_of_junction_words + number_of_disjunction_words) == (len(tables_of_from) - 1):
            real_tables_of_from = tables_of_from
        elif (number_of_junction_words + number_of_disjunction_words) < (len(tables_of_from) - 1):
            real_tables_of_from = tables_of_from[:(number_of_junction_words + number_of_disjunction_words + 1)]
            # here, there are may be also table in where section, the parsing task is more complicated
        elif (number_of_junction_words + number_of_disjunction_words) > (len(tables_of_from) - 1):
            raise ParsingException("More junction and disjunction keywords than table name in FROM!")

        for table in real_tables_of_from:
            query = Query()
            query.set_from(From(table))
            join_object = None
            join_object = Join()
            for column in columns_of_select:
                if column not in self.database_dico[table]:
                    foreign_tables = self.get_tables_of_column(column)
                    for foreign_table in foreign_tables:
                        join_object.add_table(foreign_table)
            query.set_join(join_object)
            queries.append(query)

        return queries

    def get_tables_of_column(self, column):
        tmp_table = []
        for table in self.database_dico:
            if column in self.database_dico[table]:
                 tmp_table.append(table)
        return tmp_table
    
    def parse_where(self, number_of_where_column, phrase):
        where_object = Where()
        return where_object
