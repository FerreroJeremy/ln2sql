import StringIO
import sys,re
import unittest
from ln2sql import main as ln2sql_main


class SimplisticTest(unittest.TestCase):

    def _cleanOutput(self, s):
        s = s.split("SELECT")[1]        # remove table schema
        s = re.sub("\\033.*?m", "", s)  # remove color codes
        s = s.replace('\n',' ')         # remove '\n'
        s = s.split(';')[0]             # remove spaces after ;
        s = "SELECT" + s + ';'          # put back lost SELECT and ';'
        return s

    def test_main(self):
        tests = [
            {
                'input': 'List me the info of city table',
                'sqlDump': './database/city.sql',
                'output': 'SELECT * FROM city;'
            },
            {
                'input': 'What is the number of the city in this database?',
                'sqlDump': './database/city.sql',
                'output': 'SELECT COUNT(*) FROM city;'
            },
            {
                'input': 'Tell me all id from city',
                'sqlDump': './database/city.sql',
                'output': 'SELECT city.id FROM city;'
            },
            {
                'input': 'What are the name of emp',
                'sqlDump': './database/city.sql',
                'output': 'SELECT emp.name FROM emp;'
            },
            {
                'input': 'List all name and score of all emp',
                'sqlDump': './database/city.sql',
                'output': 'SELECT emp.name, emp.score FROM emp;'
            },
            {
                'input': 'Count how many city there are where the name is Matthew ?',
                'sqlDump': './database/city.sql',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON emp.cityId = city.id WHERE emp.name = 'matthew';"
            },
            {
                'input': 'What is the emp with the name is rupinder ?',
                'sqlDump': './database/city.sql',
                'output': "SELECT * FROM emp WHERE emp.name = 'rupinder';"
            },
            {
                'input': 'What is the cityName and the score of the emp whose name is rupinder',
                'sqlDump': './database/city.sql',
                'output': "SELECT city.cityName, emp.score FROM emp INNER JOIN city ON emp.cityId = city.id WHERE emp.name = 'matthew';"
            },
            {
                'input': 'Count how many city there are where the score is greater than 2 ?',
                'sqlDump': './database/city.sql',
                'output': "SELECT COUNT(*) FROM city INNER JOIN emp ON emp.cityId = city.id WHERE emp.score > '2';"
            },
            {
                'input': '',
                'sqlDump': './database/city.sql',
                'output': ''
            },
            {
                'input': '',
                'sqlDump': './database/city.sql',
                'output': ''
            },
            {
                'input': '',
                'sqlDump': './database/city.sql',
                'output': ''
            },
            {
                'input': '',
                'sqlDump': './database/city.sql',
                'output': ''
            },
        ]

        for test in tests:
            capturedOutput = StringIO.StringIO()
            sys.stdout = capturedOutput
            ln2sql_main(['-d', test['sqlDump'], '-l',
                         './lang/english.csv', '-i', test['input']])
            sys.stdout = sys.__stdout__

            self.assertEqual(
                self._cleanOutput(capturedOutput.getvalue()),
                test['output'])

if __name__ == '__main__':
    unittest.main()
