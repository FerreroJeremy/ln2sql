# -*- coding: utf-8 -*

import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import unicodedata
from Exception import ParsingException
from Exception import GeneratingException

class Grammar:
    database_object = None
    database_dico = None
    language = None

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
        
        words = re.findall(r"[\w,.]+", self.remove_accents(sentence))

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
        
        self.parse_from(tables_of_from, from_phrase, columns_of_select, columns_of_where)
        self.parse_select(number_of_select_column, select_phrase)
        self.parse_where(number_of_where_column, where_phrase)

    def parse_select(self, number_of_select_column, phrase):
        is_count_select_query = False

        for count_keyword in self.count_keywords:
            if count_keyword in phrase:
                is_count_select_query = True

        if is_count_select_query:
            print 'Count select phrase !'
            if number_of_select_column == 0: # select count(*)
                print 'Select phrase : ' + ' '.join(phrase)
            elif number_of_select_column == 1: # one-column count select
                print 'Select phrase : ' + ' '.join(phrase)
            else: # multi-column count select
                print 'Select phrase : ' + ' '.join(phrase)
        else:
            print 'Classic select'
            if number_of_select_column == 0: # select *
                print 'Select phrase : ' + ' '.join(phrase)
            elif number_of_select_column == 1: # one-column select
                print 'Select phrase : ' + ' '.join(phrase)
            else: # multi-column select
                print 'Select phrase : ' + ' '.join(phrase)
    
    def parse_from(self, tables_of_from, phrase, columns_of_select, columns_of_where):
        if len(tables_of_from) == 0:
            raise ParsingException("No table name found in sentence!")

        print 'From phrase : ' + ' '.join(phrase)

        real_tables_of_from =[]
        real_tables_of_join =[]

        if  len(tables_of_from) == 1:
            print 'Simple query on one table'
            real_tables_of_from = tables_of_from
        else:
            number_of_junction_words = 0
            number_of_disjunction_words = 0

            for junction_keyword in self.junction_keywords:
                if junction_keyword in phrase:
                    number_of_junction_words += 1

            for disjunction_keyword in self.disjunction_keywords:
                if disjunction_keyword in phrase:
                    number_of_disjunction_words += 1

            if (number_of_junction_words + number_of_disjunction_words) >= 1:
                if (number_of_junction_words + number_of_disjunction_words) == (len(tables_of_from) - 1):
                    print 'Only multi query'
                    real_tables_of_from = tables_of_from
                elif (number_of_junction_words + number_of_disjunction_words) < (len(tables_of_from) - 1):
                    print 'Multi query and TIER'
                    real_tables_of_from = tables_of_from[:(number_of_junction_words + number_of_disjunction_words + 1)]
                elif (number_of_junction_words + number_of_disjunction_words) > (len(tables_of_from) - 1):
                    raise ParsingException("More junction and disjunction keywords than table name in FROM!")
            else:
                print 'No junction or disjunction keywords in FROM : No multi query but several table in FROM : TIER'
                real_tables_of_from = tables_of_from[0]

        for table in real_tables_of_from:
			for column in columns_of_select:
				necessary_joint = self.is_there_a_necessary_joint(column, table)
				if necessary_joint:
					possible_joint = self.is_there_a_possible_joint(column, table)
					return
					if not possible_joint:
						raise ParsingException("Query on column(s) inaccessible from the table of the FROM")
					real_tables_of_join.append(table)

    def is_there_a_necessary_joint(self, column, table):
        if column not in self.database_dico[table]:
            print column + ' is not in ' + table
            return True

    def get_tables_of_column(self, column):
    	tmp_table = []
        for table in self.database_dico:
        	if column in self.database_dico[table]:
        		tmp_table.append(table)
        return tmp_table

    def get_primary_keys_of_table(self, table):
    	primary_keys_of = self.database_object.get_primary_keys_by_table()
    	return primary_keys_of[table]

    def is_there_a_possible_joint(self, column, table):
    	tables_containing_the_column = self.get_tables_of_column(column)
    	for table_containing_the_column in tables_containing_the_column:
    		link = self.is_there_a_possible_joint_between_two_table(table_containing_the_column, table)

        if link:
            return True
        else: 
            return False

    def between_two_table(self, table_one, table_two):
    	primary_keys_of_table_one = self.get_primary_keys_of_table(table_one)
    	for primary_key in primary_keys_of_table_one:
    		if primary_key in self.database_dico[table_two]:
    			return True
    	return False
    
    def is_there_a_possible_joint_between_two_table(self, table_one, table_two):
    	for table in self.database_dico:
    		if table_one != table:
    			res = self.between_two_table(table_one, table_two)
    			if res:
    				return True
    			else:
    				return
    				

    def parse_tier(self, phrase):
        return
    
    def parse_where(self, number_of_where_column, phrase):
        if number_of_where_column == 0:
            return
        else:
            print 'Where phrase : ' + ' '.join(phrase)
