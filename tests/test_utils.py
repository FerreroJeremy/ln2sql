import os

from ln2sql.parser import Parser
from ln2sql.stopwordFilter import StopwordFilter

THESAURUS_PATH = os.path.join(BASE_PATH, 'ln2sql/thesaurus_store/')


def test_parser_sort_length():
    input_list = ['len2 len2', 'len1', 'len3 len3 len3']
    expected = ['len3 len3 len3', 'len2 len2', 'len1']
    assert Parser.transformation_sort(input_list) == expected

def test_parser_sort_length_lexical():
    input_list = ['len2 len2', 'len1', 'len3 len3 len3', 'alen3 alen3 alen3']
    expected = ['alen3 alen3 alen3', 'len3 len3 len3', 'len2 len2', 'len1']
    assert Parser.transformation_sort(input_list) == expected

def test_english_stopword_filter():
    StopwordFilter.load(THESAURUS_PATH + 'th_english.dat')
    input_sentence = 'The cat drinks milk when the dog enter in the room and his master look the TV of the hostel'
    expected = 'cat drinks milk dog enter room master tv hostel'
    assert StopwordFilter.filter(input_sentence) == expected

def test_french_stopword_filter():
    StopwordFilter.load(THESAURUS_PATH + 'th_french.dat')
    input_sentence = "Le chat boit du lait au moment où le chien rentre dans la maison et que son maître regarde la TV de l'hôtel"
    expected = 'chat boit lait chien rentre maison maitre regarde tv hotel'
    assert StopwordFilter.filter(input_sentence) == expected