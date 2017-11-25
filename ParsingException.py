import sys
import unicodedata

from constants import color


class ParsingException(Exception):
    reason = ''
    
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return color.BOLD + color.RED + self.reason + color.END
