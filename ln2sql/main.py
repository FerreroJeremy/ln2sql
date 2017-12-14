import argparse

from .ln2sql import Ln2sql

def main():
    arg_parser = argparse.ArgumentParser(description='A Utility to convert Natural Language to SQL query')
    arg_parser.add_argument('-d', '--database', help='Path to SQL dump file', required=True)
    arg_parser.add_argument('-l', '--language', help='Path to language configuration file', required=True)
    arg_parser.add_argument('-i', '--sentence', help='Input sentence to parse', required=True)
    arg_parser.add_argument('-j', '--json_output', help='path to JSON output file', default=None)
    arg_parser.add_argument('-t', '--thesaurus', help='path to thesaurus file', default=None)
    arg_parser.add_argument('-s', '--stopwords', help='path to stopwords file', default=None)

    args = arg_parser.parse_args()

    Ln2sql(
        database_path=args.database,
        language_path=args.language,
        input_sentence=args.sentence,
        json_output_path=args.json_output,
        thesaurus_path=args.thesaurus,
        stopwords_path=args.stopwords,
    )


if __name__ == '__main__':
    main()
