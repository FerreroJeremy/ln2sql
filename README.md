# ln2sql

ln2sql is a tool to query a database in natural language, as described in the following French paper (which can be found in the <i>docs/</i> directory):

<i><a rel="license" href="https://www.researchgate.net/publication/278965118_fr2sql_Interrogation_de_bases_de_donnees_en_francais">Benoît Couderc and Jérémy Ferrero. fr2sql : Database Query in French. (fr2sql : Interrogation de bases de données en français [in French]). In Proceedings of the 17th RECITAL (affiliated with the 22th TALN Conference). June 2015. Caen, France. ATALA. pp.1-12 </a></i>

In view to learn Python, I recently decided to implement our originally PHP project in Python. In addition, that will allow me to share the tool with the English-speaking community by making it public available here. The languages provided are for now English and French.

### Extra features

- [X] Load a database schema from SQL dump
- [X] Import a personal thesaurus (<a rel="thesaurus" href="http://extensions.openoffice.org/en/search?f%5B0%5D=field_project_tags%3A157">OpenOffice template</a>)
- [X] Import a personal stop word list
- [X] Print a query structure in JSON
- [X] Exception and error handling
- [X] Graphical User Interface
- [X] Multi-threading

### SQL statement supported

- [ ] one-column select
- [ ] multi-column select
- [ ] table select
- [ ] count select
- [ ] inner join
- [ ] where
- [ ] comparison
- [ ] junction
- [ ] disjunction
- [ ] cross-condition
- [ ] sum
- [ ] avg
- [ ] min
- [ ] max
- [ ] between
- [ ] order by
- [ ] group by
- [ ] multi query
- [ ] date support
- [ ] negation support

### Usage

You can directly use the python wrapper by the following way:
```
usage: ./ln2sql.py -d <path> -l <language> -i <input-sentence> [-t] [-j <path>]
-h						print this help message
-d <path>				path to sql dump file
-l <language>			language of the input sentence
-i <input-sentence>		input sentence to parse
-j <path>				path to JSON output file
-t						use thesaurus
```
example of usage:
```
./ln2sql.py -i "What is the number of students?" -l english -d ./database/tal.sql -j output.json
```
or by graphical interface by typing the following command:
```
./ln2sql_gui.py
```
a window like the one below will appear:
<p align="center">
<img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/graphical_user_interface.png">
</p>

### JSON output format

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
			  "operator": "==",
			  "value": "DOe"
			},
			{ "operator": "or" },
			{ "column": "age",
			  "operator": ">=",
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
### Conception

<p align="center">
<img src="https://raw.githubusercontent.com/FerreroJeremy/ln2sql/master/docs/entity_mvc_class_diagram.png">
</p>
The tool is implemented under the Model-View-Controller pattern. The diagram is an entity embedding class diagram, not all relations appear in this one; Each packaged class is a file. The classes imported from the Python Standard Library like Tkinter, Thread, sys or unicodedata do not appear in the diagram.

<br/>

### <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /> License

This tool is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
