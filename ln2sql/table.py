from .column import Column


class Table:
    def __init__(self, name='', columns=None, equivalences=None):
        self._name = name

        if not columns:
            columns = []
        self.columns = columns

        if not equivalences:
            equivalences = []
        self.equivalences = equivalences

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def get_number_of_columns(self):
        return len(self.columns)

    def get_columns(self):
        return self.columns

    def get_column_by_name(self, column_name):
        for column in self.columns:
            if column.name == column_name:
                return column

    def add_column(self, column_name, column_type, column_equivalences):
        self.columns.append(Column(column_name, column_type, column_equivalences))

    def get_equivalences(self):
        return self.equivalences

    def add_equivalence(self, equivalence):
        self.equivalences.append(equivalence)

    def is_equivalent(self, word):
        if word in self.equivalences:
            return True
        else:
            return False

    def get_primary_keys(self):
        primary_keys = []
        for column in self.columns:
            if column.is_primary():
                primary_keys.append(column)
        return primary_keys

    def get_primary_key_names(self):
        primary_keys = []
        for column in self.columns:
            if column.is_primary():
                primary_keys.append(column.name)
        return primary_keys

    def add_primary_key(self, primary_key_column):
        for column in self.columns:
            if column.name == primary_key_column:
                column.set_as_primary()

    def get_foreign_keys(self):
        foreign_keys = []
        for column in self.columns:
            if column.is_foreign():
                foreign_keys.append(column)
        return foreign_keys

    def get_foreign_key_names(self):
        foreign_keys = []
        for column in self.columns:
            if column.is_foreign():
                foreign_keys.append(column.name)
        return foreign_keys

    def add_foreign_key(self, column_name, foreign_table, foreign_column):
        for column in self.columns:
            if column.name == column_name:
                column.set_as_foreign({'foreign_table': foreign_table, 'foreign_column': foreign_column})
