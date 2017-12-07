class Column:
    def __init__(self, name='', type=None, equivalences=None):
        self._name = name

        if not type:
            type = []
        self._type = type

        if not equivalences:
            equivalences = []
        self._equivalences = equivalences

        self.primary = False
        self.foreign = False

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def add_type(self, type):
        self.type.append(type)

    @property
    def equivalences(self):
        return self._equivalences

    def add_equivalence(self, equivalence):
        self.equivalences.append(equivalence)

    def is_equivalent(self, word):
        if word in self.equivalences:
            return True
        else:
            return False

    def is_primary(self):
        return self.primary

    def set_as_primary(self):
        self.primary = True

    def is_foreign(self):
        return self.foreign

    def set_as_foreign(self, references):
        self.foreign = references
