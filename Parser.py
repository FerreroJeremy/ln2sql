# -*- coding: utf-8 -*

import re
import sys
import unicodedata
from threading import Thread
from ParsingException import ParsingException
from Query import *

reload(sys)
sys.setdefaultencoding("utf-8")

class SelectParser(Thread):
    def __init__(self, columns_of_select, tables_of_from, phrase, count_keywords, sum_keywords, average_keywords, max_keywords, min_keywords, database_dico):
        Thread.__init__(self)
        self.select_objects = []
        self.columns_of_select = columns_of_select
        self.tables_of_from = tables_of_from
        self.phrase = phrase
        self.count_keywords = count_keywords
        self.sum_keywords = sum_keywords
        self.average_keywords = average_keywords
        self.max_keywords = max_keywords
        self.min_keywords = min_keywords
        self.database_dico = database_dico

    def get_tables_of_column(self, column):
        tmp_table = []
        for table in self.database_dico:
            if column in self.database_dico[table]:
                 tmp_table.append(table)
        return tmp_table

    def run(self):
        for table_of_from in self.tables_of_from:
            self.select_object = Select()
            is_count = False
            number_of_select_column = len(self.columns_of_select)

            if number_of_select_column == 0:
                for count_keyword in self.count_keywords:
                    if count_keyword in self.phrase:
                        is_count = True

                if is_count:
                    self.select_object.add_column(None, 'COUNT')
                else:
                    self.select_object.add_column(None, None)
            else:
                select_phrases = []
                previous_index = 0
                for i in range(0,len(self.phrase)):
                    if self.phrase[i] in self.columns_of_select:
                        select_phrases.append(self.phrase[previous_index:i+1])
                        previous_index = i+1

                select_phrases.append(self.phrase[previous_index:])

                for i in range(0, len(select_phrases)):
                    select_type = None
                    phrase = ' '.join(select_phrases[i])

                    for keyword in self.average_keywords:
                        if keyword in phrase:
                            select_type = 'AVG'
                    for keyword in self.count_keywords:
                        if keyword in phrase:
                            select_type = 'COUNT'
                    for keyword in self.max_keywords:
                        if keyword in phrase:
                            select_type = 'MAX'
                    for keyword in self.min_keywords:
                        if keyword in phrase:
                            select_type = 'MIN'
                    for keyword in self.sum_keywords:
                        if keyword in phrase:
                            select_type = 'SUM'

                    if (i != len(select_phrases)-1) or (select_type is not None):
                        if i >= len(self.columns_of_select):
                            column = None
                        else:
                            one_table_of_column = self.get_tables_of_column(self.columns_of_select[i])[0]
                            tables_of_column = self.get_tables_of_column(self.columns_of_select[i])
                            if table_of_from in tables_of_column:
                                column = str(table_of_from) + '.' + str(self.columns_of_select[i])
                            else:
                            	column = str(one_table_of_column) + '.' + str(self.columns_of_select[i])
                        self.select_object.add_column(column, select_type)

            self.select_objects.append(self.select_object)


    def join(self):
        Thread.join(self)
        return self.select_objects

class FromParser(Thread):
    def __init__(self, tables_of_from, columns_of_select, columns_of_where, database_object):
        Thread.__init__(self)
        self.queries = []
        self.tables_of_from = tables_of_from
        self.columns_of_select = columns_of_select
        self.columns_of_where = columns_of_where
        self.database_object = database_object
        self.database_dico = self.database_object.get_tables_into_dictionnary()

    def get_tables_of_column(self, column):
        tmp_table = []
        for table in self.database_dico:
            if column in self.database_dico[table]:
                 tmp_table.append(table)
        return tmp_table

    def intersect(self, a, b):
        return list(set(a) & set(b))

    def difference(self, a, b):
        differences = []
        for _list in a:
            if _list not in b:
               differences.append(_list)
        return differences

    def is_direct_join_is_possible(self, table_src, table_trg):
        join = []
        pk_table_src = self.database_object.get_primary_keys_of_table(table_src)
        pk_table_trg = self.database_object.get_primary_keys_of_table(table_trg)
        match_pk_table_src_with_table_trg = self.intersect(pk_table_src, self.database_dico[table_trg])
        match_pk_table_trg_with_table_src = self.intersect(pk_table_trg, self.database_dico[table_src])
        
        if len(match_pk_table_src_with_table_trg) >=1:
            return [table_src, match_pk_table_src_with_table_trg[0], table_trg]
        elif len(match_pk_table_trg_with_table_src) >= 1:
            return [table_src, match_pk_table_trg_with_table_src[0], table_trg]

    def get_all_direct_linked_tables_of_a_table(self, table_src):
        links = []
        for table_trg in self.database_dico:
            if table_trg != table_src:
                link = self.is_direct_join_is_possible(table_src, table_trg)
                if link is not None:
                    links.append(link)
        return links

    def is_join(self, historic, table_src, table_trg):
        historic = historic
        links = self.get_all_direct_linked_tables_of_a_table(table_src)

        differences = []
        for join in links:
            if join[2] not in historic:
               differences.append(join)
        links = differences 

        for join in links:
            if join[2] == table_trg:
                return [0, join]

        path = []
        historic.append(table_src)

        for join in links:
            result = [1, self.is_join(historic, join[2], table_trg)]
            if result[1] != []:
                if result[0] == 0:
                    path.append(result[1])
                    path.append(join)
                else:
                    path = result[1]
                    path.append(join)
        return path

    def get_link(self, table_src, table_trg):
        path = self.is_join([], table_src, table_trg)
        if len(path) > 0:
            path.pop(0)
            path.reverse()
        return path

    def unique(self, _list):
        return [list(x) for x in set(tuple(x) for x in _list)]

    def unique_ordered(self, _list):
        frequency = []
        for element in _list:
            if element not in frequency:
                frequency.append(element)
        return frequency


    def run(self):
        self.queries = []

        for table_of_from in self.tables_of_from:
            links = []
            query = Query()
            query.set_from(From(table_of_from))
            join_object = Join()
            for column in self.columns_of_select:
                if column not in self.database_dico[table_of_from]:
                    foreign_table = self.get_tables_of_column(column)[0]
                    join_object.add_table(foreign_table)
                    link = self.get_link(table_of_from, foreign_table)
                    links.extend(link)
            for column in self.columns_of_where:
                if column not in self.database_dico[table_of_from]:
                    foreign_table = self.get_tables_of_column(column)[0]
                    join_object.add_table(foreign_table)
                    link = self.get_link(table_of_from, foreign_table)
                    links.extend(link)
            join_object.set_links(self.unique_ordered(links))
            query.set_join(join_object)
            self.queries.append(query)
            if len(join_object.get_tables()) > len(join_object.get_links()):
                self.queries = None

    def join(self):
        Thread.join(self)
        return self.queries

class WhereParser(Thread):
    def __init__(self, number_of_where_column, phrase):
        Thread.__init__(self)
        self.where_object = None

    def run(self):
        self.where_object = Where()

    def join(self):
        Thread.join(self)
        return self.where_object

class GroupByParser(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.group_by_object = None

    def run(self):
        self.group_by_object = GroupBy()

    def join(self):
        Thread.join(self)
        return self.group_by_object

class OrderByParser(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.order_by_object = None

    def run(self):
        self.order_by_object = OrderBy()

    def join(self):
        Thread.join(self)
        return self.order_by_object

class Parser:
    database_object = None
    database_dico = None
    language = None
    thesaurus_object = None

    count_keywords = []
    sum_keywords = []
    average_keywords = []
    max_keywords = []
    min_keywords = []
    junction_keywords = []
    disjunction_keywords = []
    greater_keywords = []
    less_keywords = []
    between_keywords = []
    order_by_keywords = []
    group_by_keywords = []
    negation_keywords = []

    def __init__(self, database, config):
        self.database_object = database
        self.database_dico = self.database_object.get_tables_into_dictionnary()

        self.count_keywords = config.get_count_keywords()
        self.sum_keywords = config.get_sum_keywords()
        self.average_keywords = config.get_avg_keywords()
        self.max_keywords = config.get_max_keywords()
        self.min_keywords = config.get_min_keywords()
        self.junction_keywords = config.get_junction_keywords()
        self.disjunction_keywords = config.get_disjunction_keywords()
        self.greater_keywords = config.get_greater_keywords()
        self.less_keywords = config.get_less_keywords()
        self.between_keywords = config.get_between_keywords()
        self.order_by_keywords = config.get_order_by_keywords()
        self.group_by_keywords = config.get_group_by_keywords()
        self.negation_keywords = config.get_negation_keywords()

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
                    if (number_of_table != 0) and (number_of_where_column == 0) and (i == (len(words)-1)):
                        from_phrase = words[len(select_phrase):]

        where_phrase = words[len(select_phrase) + len(from_phrase):]
        
        if (number_of_select_column + number_of_table + number_of_where_column) == 0:
            raise ParsingException("No keyword found in sentence!")

        if len(tables_of_from) > 0:
            from_phrases = []
            previous_index = 0
            for i in range(0,len(from_phrase)):
                if from_phrase[i] in tables_of_from:
                    from_phrases.append(from_phrase[previous_index:i+1])
                    previous_index = i+1

            last_junction_word_index = -1

            for i in range(0, len(from_phrases)):
                number_of_junction_words = 0
                number_of_disjunction_words = 0

                for word in from_phrases[i]:
                    if word in self.junction_keywords:
                        number_of_junction_words += 1
                    if word in self.disjunction_keywords:
                        number_of_disjunction_words += 1

                if (number_of_junction_words + number_of_disjunction_words) > 0:
                    last_junction_word_index = i

            if last_junction_word_index == -1:
                from_phrase = sum(from_phrases[:1], [])
                where_phrase = sum(from_phrases[1:], []) + where_phrase
            else:
                 from_phrase = sum(from_phrases[:last_junction_word_index+1], [])
                 where_phrase = sum(from_phrases[last_junction_word_index+1:], []) + where_phrase

        real_tables_of_from = []

        for word in from_phrase:
            if word in tables_of_from:
                real_tables_of_from.append(word)
        tables_of_from = real_tables_of_from

        if len(tables_of_from) == 0:
            raise ParsingException("No table name found in sentence!")

        select_parser = SelectParser(columns_of_select, tables_of_from, select_phrase, self.count_keywords, self.sum_keywords, self.average_keywords, self.max_keywords, self.min_keywords, self.database_dico)
        from_parser = FromParser(tables_of_from, columns_of_select, columns_of_where, self.database_object)
        where_parser = WhereParser(number_of_where_column, where_phrase)
        group_by_parser = GroupByParser()
        order_by_parser = OrderByParser()

        select_parser.start()
        from_parser.start()
        where_parser.start()
        group_by_parser.start()
        order_by_parser.start()

        queries = from_parser.join()

        if queries is None:
            raise ParsingException("There is at least one unattainable column from the table of FROM!")

        select_objects = select_parser.join()
        where_object = where_parser.join()
        group_by_object = group_by_parser.join()
        order_by_object = order_by_parser.join()

        for i in range(0, len(queries)):
            query = queries[i]
            query.set_select(select_objects[i])
            query.set_where(where_object)
            query.set_group_by(group_by_object)
            query.set_order_by(order_by_object)

        return queries
