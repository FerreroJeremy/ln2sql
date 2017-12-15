import os
import re

from ln2sql.ln2sql import Ln2sql

DATABASE_PATH = './ln2sql/database/'
LANG_PATH = './ln2sql/lang/'
THESAURUS_PATH = './ln2sql/thesaurus/'


def _clean_output(s):
    s = s.split("SELECT")[1]  # remove table schema
    s = re.sub("\\033.*?m", "", s)  # remove color codes
    s = s.replace('\n', ' ')  # remove '\n'
    s = s.split(';')[0]  # remove spaces after ;
    s = "SELECT" + s + ';'  # put back lost SELECT and ';'
    return s


def englishThesaurusUsing():
    englishThesaurusUsing = [

    ]


def frenchThesaurusUsing():
    frenchThesaurusUsing = [
        {
            'input': "Compte le nombre d'étudiant",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT COUNT(*) FROM eleve;"
        },
        {
            'input': "Compte le nombre des dénomination des étudiant",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT COUNT(eleve.nom) FROM eleve;"
        },
        {
            'input': "Quelles sont les ancienneté et les dénomination des élève ?",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT eleve.age, eleve.nom FROM eleve;"
        },
        {
            'input': "Quelles sont les ancienneté et les dénomination des étudiant ?",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT eleve.age, eleve.nom FROM eleve;"
        },
        {
            'input': "Quelles sont les salle des classe",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT classe.salle FROM classe;"
        },
        {
            'input': "Quelles sont les salle des cours",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT classe.salle FROM classe;"
        },
        {
            'input': "Quelles sont les pièce des cours",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT classe.salle FROM classe;"
        },
        {
            'input': "Compte les dénomination des étudiant dont les dénomination sont BELLE",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT COUNT(eleve.nom) FROM eleve WHERE eleve.nom = 'belle';"
        },
        {
            'input': "Compte les dénomination des étudiant dont les dénomination sont BELLE et l'ancienneté est 25",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT COUNT(eleve.nom) FROM eleve WHERE eleve.nom = 'belle' AND eleve.age = '25';"
        }
    ]
    for test in frenchThesaurusUsing:
        assert _clean_output(Ln2sql(test['database'], test['language'], thesaurus_path=test['thesaurus']).get_query(test['input'])) == test['output']

def notImplementedYet():
    notImplementedYet = [
        {
            'input': "Quel est le cours où la pièce est B45",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'thesaurus': THESAURUS_PATH + 'th_french.dat',
            'output': "SELECT * FROM classe WHERE classe.salle = 'b45';"
        }
    ]
