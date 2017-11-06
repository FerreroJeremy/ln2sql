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
                'input': 'city',
                'sqlDump': './database/city.sql',
                'output': 'SELECT * FROM city;'
            },
            {
                'input': 'cityName from city',
                'sqlDump': './database/city.sql',
                'output': 'SELECT city.cityName FROM city;'
            },
            {
                'input': 'all id from city',
                'sqlDump': './database/city.sql',
                'output': 'SELECT city.id FROM city;'
            },
            {
                'input': 'all name of emp',
                'sqlDump': './database/city.sql',
                'output': 'SELECT emp.name FROM emp;'
            },
            {
                'input': 'all name and score of all emp',
                'sqlDump': './database/city.sql',
                'output': 'SELECT emp.name, emp.score FROM emp;'
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
