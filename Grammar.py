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
    
    def __init__(self, database=None):
        if database is not None:
            self.database_object = database
            self.database_dico = self.database_object.get_tables_into_dictionnary()

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
        select_phrase = ''
        from_phrase = ''
        where_phrase = ''
        
        words = re.findall(r"[\w,.]+", self.remove_accents(sentence))

        for i in range(0, len(words)):
            if words[i] in self.database_dico:
                if number_of_table == 0:
                    select_phrase = words[:i]
                number_of_table+=1
                last_table_position = i
            for table in self.database_dico:
                if words[i] in self.database_dico[table]:
                    if number_of_table == 0:
                        number_of_select_column+=1
                    else:
                        if number_of_where_column == 0:
                            from_phrase = words[len(select_phrase):last_table_position+1]
                        number_of_where_column+=1
                    break
                else:
                    if number_of_table != 0 and number_of_where_column == 0 and i == (len(words)-1):
                        from_phrase = words[len(select_phrase):]

        where_phrase = words[len(select_phrase) + len(from_phrase):]
        
        if (number_of_select_column + number_of_table + number_of_where_column) == 0:
            raise ParsingException("No keyword find in sentence !")
        
        self.parse_from(number_of_table, from_phrase)
        self.parse_select(number_of_select_column, select_phrase)
        self.parse_where(number_of_where_column, where_phrase)

    def parse_select(self, number_of_select_column, phrase):
        ''' TODO : count select '''
        if number_of_select_column == 0: # select *
            print 'Select phrase : ' + ' '.join(phrase)
        elif number_of_select_column == 1: # one-column select
            print 'Select phrase : ' + ' '.join(phrase)
        else: # multi-column select
            print 'Select phrase : ' + ' '.join(phrase)
    
    def parse_from(self, number_of_table, phrase):
        if number_of_table == 0:
            raise ParsingException("No table name find in sentence !")
        if number_of_table == 1: # simple from
            print 'From phrase : ' + ' '.join(phrase)
        else: # there is a tier section
            print 'From phrase : ' + ' '.join(phrase)
    
    def parse_tier(self, phrase):
        print 'Tier phrase : ' + ' '.join(phrase)
    
    def parse_where(self, number_of_where_column, phrase):
        if number_of_where_column == 0:
            return
        else:
            print 'Where phrase : ' + ' '.join(phrase)
