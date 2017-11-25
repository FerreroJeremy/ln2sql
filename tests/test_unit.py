import re

import pytest

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


def test_main():
    correctTest = [
        {
            'input': 'List me the info of city table',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': 'SELECT * FROM city;'
        },
        {
            'input': 'What is the number of the city in this database?',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': 'SELECT COUNT(*) FROM city;'
        },
        {
            'input': 'Tell me all id from city',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': 'SELECT city.id FROM city;'
        },
        {
            'input': 'What are the name of emp',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': 'SELECT emp.name FROM emp;'
        },
        {
            'input': 'List all name and score of all emp',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': 'SELECT emp.name, emp.score FROM emp;'
        },
        {
            'input': 'Count how many city there are where the name is Matthew ?',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.name = 'matthew';"
        },
        {
            'input': 'What is the emp with the name is rupinder ?',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT * FROM emp WHERE emp.name = 'rupinder';"
        },
        {
            'input': 'What is the cityName and the score of the emp whose name is matthew',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'matthew';"
        },
        {
            'input': 'Count how many city there are where the score is greater than 2 ?',
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.score > '2';"
        },
        {
            'input': "Show data for city where cityName is 'Pune Agra'",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT * FROM city WHERE city.cityName = 'pune agra';"
        },
        {
            'input': "Show data for city where cityName is not Pune and id like 1",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT * FROM city WHERE city.cityName != 'pune' AND city.id LIKE '%1%';"
        },
        {
            'input': "What is the cityName and the score of the emp whose name is rupinder",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'rupinder';"
        },
        {
            'input': "count how many city there are ordered by name",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name ASC;"
        },
        {
            'input': "count how many city there are ordered by name in descending order and ordered by score in ascending order",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
        },
        {
            'input': "count how many city there are ordered by name in descending order and ordered by score?",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
        },
        {
            'input': "Combien y a t'il de client ?",
            'database': DATABASE_PATH + 'hotel.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT COUNT(*) FROM client;"
        },
        {
            'input': "Combien y a t'il de client dont le nom est Jean ?",
            'database': DATABASE_PATH + 'hotel.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT COUNT(*) FROM client WHERE client.nom = 'jean';"
        },
        {
            'input': "Quel est l'age du client dont le nom est Jean ?",
            'database': DATABASE_PATH + 'hotel.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT client.age FROM client WHERE client.nom = 'jean';"
        },
        {
            'input': "Quel est l'adresse du client dont le nom est Jean et dont l'age est supérieur à 14 ?",
            'database': DATABASE_PATH + 'hotel.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT client.adresse FROM client WHERE client.nom = 'jean' AND client.age > '14';"
        },
        {
            'input': "Quel est l'adresse et le numéro de téléphone du client dont le nom est Marc et "
                     "dont l'age est supérieur à 14 groupé par adresse ?",
            'database': DATABASE_PATH + 'hotel.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT client.adresse, client.telephone FROM client WHERE client.nom = 'marc' AND c"
                      "lient.age > '14' GROUP BY client.adresse;"
        },
        {
            'input': "Quel est la moyenne d'age des eleve ?",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT AVG(eleve.age) FROM eleve;"
        },
        {
            'input': "Quels sont distinctivement les age des eleve ?",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT DISTINCT eleve.age FROM eleve;"
        },
        {
            'input': "compte distinctivement les eleve ?",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT COUNT(*) FROM eleve;"
        },
        {
            'input': "Compte distinctivement les age des eleve ?",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT COUNT(DISTINCT eleve.age) FROM eleve;"
        },
        {
            'input': "count distinctly how many city there are ordered by name in descending and ordered by score?",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
        },
        {
            'input': "Count distinctly how many different name of city there are ordered by name in descending and ordered by score?",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT COUNT(DISTINCT emp.name) FROM city INNER JOIN emp ON city.id = emp.cityId ORDER BY emp.name DESC, emp.score ASC;"
        },
        {
            'input': "What are the distinct name of city with a score equals to 9?",
            'database': DATABASE_PATH + 'city.sql',
            'language': LANG_PATH + 'english.csv',
            'output': "SELECT DISTINCT emp.name FROM city INNER JOIN emp ON city.id = emp.cityId WHERE emp.score = '9';"
        },
        {
            'input': "Compte les nom des élève dont les nom sont BELLE",
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv',
            'output': "SELECT COUNT(eleve.nom) FROM eleve WHERE eleve.nom = 'belle';"
        }
    ]

    for test in correctTest:
        assert _clean_output(
            Ln2sql(test['database'], test['language'], test['input']).get_query()
        ) == test['output']


def test_exception():
    errorTest = [
        {
            'input': 'Quel est le nom des reservation ?',  # No table name found in sentence!
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv'
        },
        {
            'input': 'Affiche moi.',  # No keyword found in sentence!
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv'
        },
        {
            'input': 'Affiche moi les étudiants',  # No keyword found in sentence!
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv'
        },
        {
            'input': "Quel est le professeur qui enseigne la matière SVT ?",
            # There is at least column `matiere` that is unreachable from table `PROFESSEUR`!
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv'
        },
        {
            'input': "compte les salle des élève",
            # There is at least column `salle` that is unreachable from table `ELEVE`!
            'database': DATABASE_PATH + 'ecole.sql',
            'language': LANG_PATH + 'french.csv'
        }
    ]
    for test in errorTest:
        with pytest.raises(Exception):
            Ln2sql(test['database'], test['language'], test['input']).get_query()
