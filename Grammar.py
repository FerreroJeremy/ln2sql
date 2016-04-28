# -*- coding: utf-8 -*

import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import unicodedata

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
        
        select_phrase = ''
        from_phrase = ''
        where_phrase = ''
        
        words = re.findall(r"[\w,.]+", self.remove_accents(sentence))
        
        print '\n'
        print 'Input sentence : ' + self.remove_accents(sentence)

        for i in range(0, len(words)):
            if words[i] in self.database_dico:
                if number_of_table == 0:
                    select_phrase = words[:i]
                number_of_table+=1
            for table in self.database_dico:
                if words[i] in self.database_dico[table]:
                    if number_of_table == 0:
                        number_of_select_column+=1
                    else:
                        if number_of_where_column == 0:
                            from_phrase = words[len(select_phrase):i]
                        number_of_where_column+=1
                    break
                else:
                    if number_of_table != 0 and number_of_where_column == 0 and i == (len(words)-1):
                        from_phrase = words[len(select_phrase):]

        where_phrase = words[len(select_phrase) + len(from_phrase):]
        
        print '\n'
        
        print 'Number of columns in SELECT : ' + str(number_of_select_column)
        print 'Number of tables : ' + str(number_of_table)
        print 'Nombre of columns in WHERE : ' + str(number_of_where_column)
        
        print '\n'
        
        self.parse_select(number_of_select_column, select_phrase)
        self.parse_from(number_of_table, from_phrase)
        self.parse_where(number_of_where_column, where_phrase)
        
        print '\n'

    def parse_select(self, number_of_select_column, phrase):
        print 'Select phrase : ' + ' '.join(phrase)
    
    def parse_from(self, number_of_table, phrase):
        print 'From phrase : ' + ' '.join(phrase)
    
    def parse_tier(self, phrase):
        print 'Tier phrase : ' + ' '.join(phrase)
    
    def parse_where(self, number_of_where_column, phrase):
        print 'Where phrase : ' + ' '.join(phrase)
