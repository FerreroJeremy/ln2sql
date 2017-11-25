import io
import sys,re
import unittest

from ln2sql import main as ln2sql_main
from ParsingException import ParsingException

class ThesaurusTest(unittest.TestCase):

    def _cleanOutput(self, s):
        s = s.split("SELECT")[1]        # remove table schema
        s = re.sub("\\033.*?m", "", s)  # remove color codes
        s = s.replace('\n',' ')         # remove '\n'
        s = s.split(';')[0]             # remove spaces after ;
        s = "SELECT" + s + ';'          # put back lost SELECT and ';'
        return s

    def test_main(self):
        thesaurusTest = [
            {
                'input': "Compte le nombre d'étudiant",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT COUNT(*) FROM eleve;"
            },
            {
                'input': "Compte le nombre des dénomination des étudiant",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT COUNT(eleve.nom) FROM eleve;"
            },
            {
                'input': "Quelles sont les ancienneté et les dénomination des élève ?",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT eleve.age, eleve.nom FROM eleve;"
            },
            {
                'input': "Quelles sont les ancienneté et les dénomination des étudiant ?",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT eleve.age, eleve.nom FROM eleve;"
            },
            {
                'input': "Quelles sont les salle des classe",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT classe.salle FROM classe;"
            },
            {
                'input': "Quelles sont les salle des cours",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT classe.salle FROM classe;"
            },
            {
                'input': "Quelles sont les pièce des cours",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT classe.salle FROM classe;"
            },
            {
                'input': "Compte les dénomination des étudiant dont les dénomination sont BELLE",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT COUNT(eleve.nom) FROM eleve WHERE eleve.nom = 'belle';"
            },
            {
                'input': "Compte les dénomination des étudiant dont les dénomination sont BELLE et l'ancienneté est 25",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT COUNT(eleve.nom) FROM eleve WHERE eleve.nom = 'belle' AND eleve.age = '25';"
            }
        ]

        thesaurusTest2 = [
            {
                'input': "Quel est le cours où la pièce est B45",
                'database': './database/ecole.sql',
                'language': './lang/french.csv',
                'thesaurus': 'thesaurus/th_french.dat',
                'output': "SELECT * FROM classe WHERE classe.salle = 'b45';"
            }
        ]

        for test in thesaurusTest:
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            ln2sql_main(['-d', test['database'], '-l', test['language'], '-i', test['input'], '-t', test['thesaurus']])
            sys.stdout = sys.__stdout__
            self.assertEqual(self._cleanOutput(capturedOutput.getvalue()), test['output'])
