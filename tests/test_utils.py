from ln2sql.parser import Parser


def test_parser_sort_length():
    input_list = ['len2 len2', 'len1', 'len3 len3 len3']
    expected = ['len3 len3 len3', 'len2 len2', 'len1']
    assert Parser.transformation_sort(input_list) == expected


def test_parser_sort_length_lexical():
    input_list = ['len2 len2', 'len1', 'len3 len3 len3', 'alen3 alen3 alen3']
    expected = ['alen3 alen3 alen3', 'len3 len3 len3', 'len2 len2', 'len1']

    assert Parser.transformation_sort(input_list) == expected
