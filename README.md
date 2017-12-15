# ln2sql

<b>ln2sql is a NLP tool to query a database in natural language.</b> The tool takes in input a database model and a sentence and translate the latter in a valid SQL statement able to query the input data model.

##### Scientific paper

The initial tool is described in the following French paper (which can be found in the `docs/` directory):

<i><a rel="license" href="https://www.researchgate.net/publication/278965118_fr2sql_Interrogation_de_bases_de_donnees_en_francais">Benoît Couderc and Jérémy Ferrero. fr2sql : Database Query in French. (fr2sql : Interrogation de bases de données en français [in French]). In Proceedings of the 17th RECITAL (affiliated with the 22th TALN Conference). June 2015. Caen, France. ATALA. pp.1-12 </a></i>

Please cite the paper if you use ln2sql.

#### Differences between the version of the paper <i>(fr2sql)</i> and this version <i>(ln2sql)</i>

ln2sql is not the state-of-the-art tool for copyright reasons. It's just a quick & dirty Python wrapper but it has some speed optimizations.

* [A data model is only learned from a parsing of a SQL dump file. Thus, <b>no database connection is needed</b>.](https://github.com/FerreroJeremy/ln2sql#database-input)

* In the paper, <a rel="tt" href="http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/">TreeTagger</a> is used to filter the words of the input sentence according to its POS tagging.
In this way, a mapping between the keywords of the input sentence and the keywords of the data model can be performed.
In ln2sql, Treegagger is left in favour of an import of personal configuration files (for [languages](https://github.com/FerreroJeremy/ln2sql#supported-languages), [stop words and synonyms](https://github.com/FerreroJeremy/ln2sql#thesaurus-and-stop-word-list)) to be more generic.

> Beware that ln2sql cannot therefore automatically solve the gender and number problem. So if the word <i>"student<b>s</b>"</i> is in the input sentence, it does not match with the table <i>"student"</i> in the model of data.
To do that, the equivalence <i>"student<b>s</b> → student"</i> must be appear in the [used thesaurus](https://github.com/FerreroJeremy/ln2sql#thesaurus-and-stop-word-list).
If you want a version using TreeTagger, a <a rel="wrapper" href="https://perso.limsi.fr/pointal/dev:treetaggerwrapper">Python wrapper</a> exists and a documentation can be found <a rel="doc" href="http://treetaggerwrapper.readthedocs.io/en/latest/">here</a>.

* [In theory, all languages can be supported.](https://github.com/FerreroJeremy/ln2sql#supported-languages)

* A grammar still parse the input sentence to generate the corresponding query structure, but now this structure is stocked in a Python class able to print [a query structure JSON file](https://github.com/FerreroJeremy/ln2sql/blob/master/README.md#json-output). Thus, the hash map for the query generation was abandoned. In addition, a multi-threading implementation was adopted.

## SQL statements supported

- [X] SELECT
	- [X] one column
	- [X] multiple columns
	- [X] all columns
	- [X] distinct select
	- [X] aggregate functions
		- [X] count-select
		- [X] sum-select
		- [X] avg-select
		- [X] min-select
		- [X] max-select
- [X] JOIN
	- [X] inner join
	- [X] natural join
- [X] WHERE
	- [X] one condition
	- [X] multiple conditions
	- [X] junction
	- [X] disjunction
	- [X] cross-condition
	- [X] operators
		- [X] equal operator
		- [X] not equal operator
		- [X] greater-than operator
		- [X] less-than operator
		- [X] like operator
		- [ ] between operator (not 100% efficient)
	- [X] aggregate functions
		- [X] sum in condition
		- [X] avg in condition
		- [X] min in condition
		- [X] max in condition
- [X] ORDER BY
	- [X] ASC
	- [X] DESC
- [X] GROUP BY
- [X] multiple queries
- [X] exception and error handling
- [ ] detection of values (not 100% efficient)

## How to use it?

#### Supported languages

The tool can deal with any language, so long as it has its configuration file (<i>i.e.</i> a file with the keywords of the language).

Language configuration files can be found in `lang/` directory. The files are CSV files. Each line represent a type of keywords. Anything before the colon is ignored. Keywords must be separated by a comma.

You can build your own language configuration file following the English and French templates.

#### Database input

To be effective ln2sql need to learn the data model of the database that the user want to query. It need to load the corresponding SQL dump file to do that.<br/>
A <a rel="dump" href="https://en.wikipedia.org/wiki/Database_dump">database dump</a> is a file containing a record of the table structure and/or the data of a database.

##### Usage of the Database class

```python
database = Database()
database.load("database/tal.sql")
database.print_me()
```
For the following SQL statements loaded, the output in the terminal looks like:
<p align="center"><img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/database_loading.png" width="700"></p>

#### Thesaurus and stop word list

You can improve the keyword filtering using a thesaurus. Thesaurus can be found in `thesaurus/` directory. You can build your own thesaurus following the <a rel="thesaurus" href="http://extensions.openoffice.org/en/search?f%5B0%5D=field_project_tags%3A157">OpenOffice template</a>.

You can improve the stop word filtering using a stop word list. You can build your own stop word list following the template of the lists in `stopwords/` directory.

#### Usage

You can directly use the python wrapper by the following way:
```
Usage:
	From the cloned source:
	python3 -m ln2sql.main -d <path> -l <path> -i <input-sentence> [-j <path>] [-t <path>] [-s <path>]
Parameters:
	-h					print this help message
	-d <path>				path to sql dump file
	-l <path>				path to language configuration file
	-i <input-sentence>			input sentence to parse
	-j <path>				path to JSON output file
	-t <path>				path to thesaurus file
	-s <path>				path to stopwords file
```
example of usage:
```
python3 -m ln2sql.main -d database_store/city.sql -l lang_store/english.csv -j output.json -i "Count how many city there are with the name blob?"
```

or by graphical interface by typing the following command:
```
python ln2sql_gui.py
```
a window like the one below will appear:
<p align="center"><img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/graphical_user_interface.png" width="600"></p>

## JSON output

With the following input:
```
What is the average age of students whose name is Doe or age over 25?
```
the output is:
```JSON
{
	"select": {
		"column": "age",
		"type": "AVG"
	},
	"from": {
		"table": "student"
	},
	"join": {

	},
	"where": {
		"conditions": [
			{ "column": "name",
			  "operator": "=",
			  "value": "Doe"
			},
			{
			  "operator": "OR"
			},
			{ "column": "age",
			  "operator": ">",
			  "value": "25"
			}
		]
	},
	"group_by": {

	},
	"order_by": {

	}
}
```

## Conception
The tool is implemented under the Model-View-Controller pattern. The classes imported from the Python Standard Library do not appear in the diagram except those required for inheritance (<i>e.g.</i> <i>Thread</i> or <i>Exception</i>).
<p align="center"><img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/mvc_class_diagram.png"></p>
The above diagram was modeled with <a rel="staruml" href="http://staruml.io/">StarUML</a>.
<br/>
<br/>
