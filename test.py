#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

from Database import Database

if __name__ == '__main__':
    database = Database()
    database.load(sys.argv[1])
    database.print_me()