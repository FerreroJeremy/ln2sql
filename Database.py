import sys, re
import unicodedata

from constants import color
from Table import Table


class Database:
    thesaurus_object = None
    tables = []
    
    def __init__(self):
        self.tables = []
        
    def set_thesaurus(self, thesaurus):
        self.thesaurus_object = thesaurus
    
    def get_number_of_tables(self):
        return len(self.tables)
    
    def get_tables(self):
        return self.tables

    def get_column_with_this_name(self, name):
        for table in self.tables:
            for column in table.get_columns():
                if column.get_name() == name:
                    return column

    def get_table_by_name(self, table_name):
        for table in self.tables:
            if table.get_name() == table_name:
                return table
    
    def get_tables_into_dictionnary(self):
        data = {}
        for table in self.tables:
            data[table.get_name()] = []
            for column in table.get_columns():
                data[table.get_name()].append(column.get_name())
        return data

    def get_primary_keys_by_table(self):
        data = {}
        for table in self.tables:
            data[table.get_name()] = table.get_primary_keys()
        return data

    def get_foreign_keys_by_table(self):
        data = {}
        for table in self.tables:
            data[table.get_name()] = table.get_foreign_keys()
        return data

    def get_primary_keys_of_table(self, table_name):
        for table in self.tables:
            if table.get_name() == table_name:
                return table.get_primary_keys()

    def get_primary_key_names_of_table(self, table_name):
        for table in self.tables:
            if table.get_name() == table_name:
                return table.get_primary_key_names()

    def get_foreign_keys_of_table(self, table_name):
        for table in self.tables:
            if table.get_name() == table_name:
                return table.get_foreign_keys()

    def get_foreign_key_names_of_table(self, table_name):
        for table in self.tables:
            if table.get_name() == table_name:
                return table.get_foreign_key_names()

    def add_table(self, table):
        self.tables.append(table)
    
    def load(self, path):
        with open(path) as f:
            content = f.read()
            tables_string = [p.split(';')[0] for p in content.split('CREATE') if ';' in p]
            for table_string in tables_string:
                if 'TABLE' in table_string:
                    table = self.create_table(table_string)
                    self.add_table(table)
            alter_tables_string = [p.split(';')[0] for p in content.split('ALTER') if ';' in p]
            for alter_table_string in alter_tables_string:
                if 'TABLE' in alter_table_string:
                    self.alter_table(alter_table_string)

    def predict_type(self, string):
        if 'int' in string.lower():
            return 'int'
        elif 'char' in string.lower() or 'text' in string.lower():
            return 'string'
        elif 'date' in string.lower():
            return 'date'
        else:
            return 'unknow'

    def create_table(self, table_string):
        lines = table_string.split("\n")
        table = Table()
        for line in lines:
            if 'TABLE' in line:
                table_name = re.search("`(\w+)`", line)
                table.set_name(table_name.group(1))
                if self.thesaurus_object is not None:
                    table.set_equivalences(self.thesaurus_object.get_synonyms_of_a_word(table.get_name()))
            elif 'PRIMARY KEY' in line:
                primary_key_columns = re.findall("`(\w+)`", line)
                for primary_key_column in primary_key_columns:
                    table.add_primary_key(primary_key_column)
            else:
                column_name = re.search("`(\w+)`", line)
                if column_name is not None:
                    column_type = self.predict_type(line)
                    if self.thesaurus_object is not None:
                        equivalences = self.thesaurus_object.get_synonyms_of_a_word(column_name.group(1))
                    else:
                        equivalences = []
                    table.add_column(column_name.group(1), column_type, equivalences)
        return table

    def alter_table(self, alter_string):
        lines = alter_string.replace('\n', ' ').split(';')
        for line in lines:
            if 'PRIMARY KEY' in line:
                table_name = re.search("TABLE `(\w+)`", line).group(1)
                table = self.get_table_by_name(table_name)
                primary_key_columns = re.findall("PRIMARY KEY \(`(\w+)`\)", line)
                for primary_key_column in primary_key_columns:
                    table.add_primary_key(primary_key_column)
            elif 'FOREIGN KEY' in line:
                table_name = re.search("TABLE `(\w+)`", line).group(1)
                table = self.get_table_by_name(table_name)
                foreign_keys_list = re.findall("FOREIGN KEY \(`(\w+)`\) REFERENCES `(\w+)` \(`(\w+)`\)", line)
                for column, foreign_table, foreign_column in foreign_keys_list:
                    table.add_foreign_key(column, foreign_table, foreign_column)

    def print_me(self):
        for table in self.tables:
            print('+-------------------------------------+')
            print("| %25s           |" % (table.get_name().upper()))
            print('+-------------------------------------+')
            for column in table.columns:
                if column.is_primary():
                    print("| 🔑 %31s           |" % (color.BOLD + column.get_name() + ' (' + column.get_type() + ')' + color.END))
                elif column.is_foreign():
                    print("| #️⃣ %31s           |" % (color.ITALIC + column.get_name() + ' (' + column.get_type() + ')' + color.END))
                else:
                    print("|   %23s           |" % (column.get_name() + ' (' + column.get_type() + ')'))
            print('+-------------------------------------+\n')
