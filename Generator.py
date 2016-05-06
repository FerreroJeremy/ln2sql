# -*- coding: utf-8 -*

import re
import sys
import unicodedata
from threading import Thread
from Exception import ParsingException
from Query import *

reload(sys)
sys.setdefaultencoding("utf-8")

class SelectGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        return

    def join(self):
        Thread.join(self)
        return

class FromGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        return

    def join(self):
        Thread.join(self)
        return self.queries

class WhereGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        return

    def join(self):
        Thread.join(self)
        return

class JoinGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        return

    def join(self):
        Thread.join(self)
        return

class GroupByGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        return

    def join(self):
        Thread.join(self)
        return

class OrderByGenerator(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        return

    def join(self):
        Thread.join(self)
        return

class Generator:

    def __init__(self):
    	return

    def generate(self, queries):
        for query in queries:
            select_object = query.get_select()
            from_object = query.get_from()
            where_object = query.get_where()
            join_object = query.get_join()
            group_by_object = query.get_group_by()
            order_by_object = query.get_order_by()

            select_generator = SelectGenerator(select_object)
            from_generator = FromGenerator(from_object)
            where_generator = WhereGenerator(where_object)
            join_generator = JoinGenerator(join_object)
            group_by_generator = GroupByGenerator(group_by_object)
            order_by_generator = OrderByGenerator(order_by_object)

            select_generator.start()
            from_generator.start()
            where_generator.start()
            join_generator.start()
            group_by_generator.start()
            order_by_generator.start()

            select_phrase = select_generator.join()
            from_phrase = from_generator.join()
            where_phrase = where_generator.join()
            join_phrase = join_generator.join()
            group_by_phrase = group_by_generator.join()
            order_by_phrase = order_by_generator.join()
