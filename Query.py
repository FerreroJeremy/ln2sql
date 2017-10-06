# -*- coding: utf-8 -*

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class Select():
	columns = []

	def __init__(self):
		self.columns = []

	def add_column(self, column, column_type):
		if [column, column_type] not in self.columns:
			self.columns.append([column, column_type])

	def get_columns(self):
		return self.columns

	def get_just_column_name(self, column):
		if column != str(None):
			return column.rsplit('.', 1)[1]
		else:
			return column

	def print_column(self, selection):
		column = selection[0]
		column_type = selection[1]

		if column is None:
			if column_type == 'COUNT':
				return color.BOLD + 'COUNT(' + color.END + '*' + color.BOLD + ')' + color.END
			else:
				return '*'
		else:
			if column_type == 'COUNT':
				return color.BOLD + 'COUNT(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'AVG':
				return color.BOLD + 'AVG(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'SUM':
				return color.BOLD + 'SUM(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'MAX':
				return color.BOLD + 'MAX(' + color.END + str(column) + color.BOLD + ')' + color.END
			elif column_type == 'MIN':
				return color.BOLD + 'MIN(' + color.END + str(column) + color.BOLD + ')' + color.END
			else:
				return str(column)

	def __str__(self):
		select_string = ''
		for i in range(0, len(self.columns)):
			if i == (len(self.columns)-1):
				select_string = select_string + str(self.print_column(self.columns[i]))
			else:
				select_string = select_string + str(self.print_column(self.columns[i])) + ', '

		return color.BOLD + 'SELECT ' + color.END + select_string

	def print_json(self, output):
		if len(self.columns) >= 1:
			if len(self.columns) == 1:
				output.write('\t"select": {\n')
				output.write('\t\t"column": "' + self.get_just_column_name(str(self.columns[0][0])) + '",\n')
				output.write('\t\t"type": "' + str(self.columns[0][1]) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"select": {\n')
				output.write('\t\t"columns": [\n')
				for i in range(0, len(self.columns)):
					if i == (len(self.columns)-1):
						output.write('\t\t\t{ "column": "' + self.get_just_column_name(str(self.columns[i][0])) + '",\n')
						output.write('\t\t\t  "type": "' + str(self.columns[i][1]) + '"\n')
						output.write('\t\t\t}\n')
					else:
						output.write('\t\t\t{ "column": "' + self.get_just_column_name(str(self.columns[i][0])) + '",\n')
						output.write('\t\t\t  "type": "' + str(self.columns[i][1]) + '"\n')
						output.write('\t\t\t},\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
		else:
			output.write('\t"select": {\n')
			output.write('\t},\n')

class From():
	table = ''

	def __init__(self, table=None):
		if table is not None:
			self.table = table
		else:
			self.table = ''

	def set_table(self, table):
		self.table = table

	def get_table(self):
		return self.table

	def __str__(self):
		return '\n' + color.BOLD + 'FROM ' + color.END + str(self.table)

	def print_json(self, output):
		if self.table != '':
			output.write('\t"from": {\n')
			output.write('\t\t"table": "' + str(self.table) + '"\n')
			output.write('\t},\n')
		else:
			output.write('\t"from": {\n')
			output.write('\t},\n')

class Join():
	tables = []
	links = []

	def __init__(self):
		self.tables = []
		self.links = []

	def add_table(self, table):
		if table not in self.tables:
			self.tables.append(table)

	def set_links(self, links):
		self.links = links

	def get_tables(self):
		return self.tables

	def get_links(self):
		return self.links

	def __str__(self):
		if len(self.links) >= 1:
			string = ''
			for i in range(0, len(self.links)):
				string += '\n' + color.BOLD + 'INNER JOIN ' + color.END + str(self.links[i][2]) + '\n' + color.BOLD + 'ON ' + color.END + str(self.links[i][0]) + '.' + str(self.links[i][1]) + ' = ' + str(self.links[i][2]) + '.' + str(self.links[i][1])
			return string
		elif len(self.tables) >= 1:
			if len(self.tables) == 1:
				return '\n' + color.BOLD + 'NATURAL JOIN ' + color.END + self.tables[0]
			else:
				string = '\n' + color.BOLD + 'NATURAL JOIN ' + color.END
				for i in range(0, len(self.tables)):
					if i == (len(self.tables)-1):
						string += str(self.tables[i])
					else:
						string += str(self.tables[i]) + ', '
				return string
		else:
			return ''

	def print_json(self, output):
		if len(self.tables) >= 1:
			if len(self.tables) == 1:
				output.write('\t"join": {\n')
				output.write('\t\t"table": "' + str(self.tables[0]) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"join": {\n')
				output.write('\t\t"tables": [')
				for i in range(0, len(self.tables)):
					if i == (len(self.tables)-1):
						output.write('"' + str(self.tables[i]) + '"')
					else:
						output.write('"' + str(self.tables[i]) + '", ')
				output.write(']\n')
				output.write('\t},\n')
		else:
			output.write('\t"join": {\n')
			output.write('\t},\n')

class Condition():
	column = ''
	column_type = ''
	operator = ''
	value = ''

	def __init__(self, column, column_type, operator, value):
		self.column = column
		self.column_type = column_type
		self.operator = operator
		self.value = value

	def get_column(self):
		return self.column

	def get_column_type(self):
		return self.column_type

	def get_operator(self):
		return self.operator

	def get_value(self):
		return self.value

	def get_in_list(self):
		return [self.column, self.column_type, self.operator, self.value]

	def get_just_column_name(self, column):
		if column != str(None):
			return column.rsplit('.', 1)[1]
		else:
			return column

	def get_column_with_type_operation(self, column, column_type):
		if column_type is None:
			return self.column
		else:
			return color.BOLD + str(column_type) + '(' + color.END + self.column + color.BOLD + ')' + color.END

	def get_pretty_operator(self, operator):
		if operator == 'BETWEEN':
			return color.BOLD + 'BETWEEN' + color.END + ' OOV ' + color.BOLD + 'AND' + color.END
		else:
			return color.BOLD + operator + color.END

	def __str__(self):
		return str(self.get_column_with_type_operation(self.column, self.column_type)) + ' ' + str(self.get_pretty_operator(self.operator)) + ' ' + str(self.value)

	def print_json(self, output):

		output.write('\t\t\t{ "column": "' + self.get_just_column_name(str(self.column)) + '",\n\t\t\t  "type": "' + str(self.column_type) + '",\n\t\t\t  "operator": "' + str(self.operator) + '",\n\t\t\t  "value": "' + str(self.value) + '"\n\t\t\t}')

class Where():
	conditions = []

	def __init__(self, clause=None):
		if clause is not None:
			self.conditions.append([None, clause])
		else:
			self.conditions = []

	def add_condition(self, junction, clause):
		self.conditions.append([junction, clause])

	def get_conditions(self):
		return self.conditions

	def __str__(self):
		string = ''

		if len(self.conditions) >= 1:
			for i in range(0, len(self.conditions)):
				if i == 0:
					string += '\n' + color.BOLD + 'WHERE' + color.END + ' ' + str(self.conditions[i][1])
				else:
					string += '\n' + color.BOLD + str(self.conditions[i][0]) + color.END + ' ' + str(self.conditions[i][1])
			
			return string
		else:
			return string

	def print_json(self, output):
		if len(self.conditions) >= 1:
			if len(self.conditions) == 1:
				output.write('\t"where": {\n')
				output.write('\t\t"condition": [\n')
				self.conditions[0][1].print_json(output)

				
				output.write('\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
			else:
				output.write('\t"where": {\n')
				output.write('\t\t"conditions": [\n')
				for i in range(0, len(self.conditions)):
					if i != 0:
						output.write('\t\t\t{\n\t\t\t  "operator": "' + str(self.conditions[i][0]) + '"\n\t\t\t},\n')
					self.conditions[i][1].print_json(output)
					if i != (len(self.conditions)-1):
						output.write(',')
					output.write('\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
		else:
			output.write('\t"where": {\n')
			output.write('\t},\n')
    
class GroupBy():
	column = None

	def __init__(self, column=None):
		if column is not None:
			self.column = column
		else:
			self.column = None

	def set_column(self, column):
		self.column = column

	def get_column(self):
		return self.column

	def get_just_column_name(self, column):
		if column != str(None):
			return column.rsplit('.', 1)[1]
		else:
			return column

	def __str__(self):
		if self.column is not None:
			return '\n' + color.BOLD + 'GROUP BY ' + color.END + str(self.column)
		else:
			return ''

	def print_json(self, output):
		if self.column is not None:
			output.write('\t"group_by": {\n')
			output.write('\t\t"column": "' + self.get_just_column_name(str(self.column)) + '"\n')
			output.write('\t},\n')
		else:
			output.write('\t"group_by": {\n')
			output.write('\t},\n')

class OrderBy():
	columns = []
	order = None

	def __init__(self, columns=None, order=None):
		if columns is not None:
			self.columns = columns
		else:
			self.columns = []

		if order is not None:
			self.order = order
		else:
			self.order = None

	def add_column(self, column):
		if column not in self.columns:
			self.columns.append(column)

	def get_columns(self):
		return self.columns

	def set_order(self, order):
		self.order = order

	def get_order(self):
		return self.order

	def get_just_column_name(self, column):
		if column != str(None):
			return column.rsplit('.', 1)[1]
		else:
			return column

	def __str__(self):
		if self.columns != []:
			string = color.BOLD + 'ORDER BY ' + color.END
			for i in range(0, len(self.columns)):
				if i == (len(self.columns)-1):
					string += self.columns[i]
				else:
					string += self.columns[i] + ', '
			if self.order == 0:
				string += color.BOLD + ' ASC' + color.END
			else:
				string += color.BOLD + ' ASC' + color.END

			return '\n' + string
		else:
			return ''

	def print_json(self, output):
		if len(self.columns) >= 1:
			if len(self.columns) == 1:
				output.write('\t"order_by": {\n')
				output.write('\t\t"order": "' + str(self.order) + '",\n')
				output.write('\t\t"column": "' + self.get_just_column_name(str(self.columns[0])) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"order_by": {\n')
				output.write('\t\t"order": "' + str(self.order) + '",\n')
				output.write('\t\t"columns": [')
				for i in range(0, len(self.columns)):
					if i == (len(self.columns)-1):
						output.write('"' + self.get_just_column_name(str(self.columns[i])) + '"')
					else:
						output.write('"' + self.get_just_column_name(str(self.columns[i])) + '", ')
				output.write(']\n')
				output.write('\t},\n')
		else:
			output.write('\t"order_by": {\n')
			output.write('\t}\n')

class Query():
	select = None
	_from = None
	join = None
	where = None
	group_by = None
	order_by = None

	def __init__(self, select=None, _from=None, join=None, where=None, group_by=None, order_by=None):
		if select is not None:
			self.select = select
		else:
			self.select = None
		if _from is not None:
			self._from = _from
		else:
			self._from = None
		if join is not None:
			self.join = join
		else:
			self.join = None
		if where is not None:
			self.where = where
		else:
			self.where = None
		if group_by is not None:
			self.group_by = group_by
		else:
			self.group_by = None
		if order_by is not None:
			self.order_by = order_by
		else:
			self.order_by = None

	def set_select(self, select):
		self.select = select

	def get_select(self):
		return self.select

	def set_from(self, _from):
		self._from = _from

	def get_from(self):
		return self._from

	def set_join(self, join):
		self.join = join

	def get_join(self):
		return self.join

	def set_where(self, where):
		self.where = where

	def get_where(self):
		return self.where

	def set_group_by(self, group_by):
		self.group_by = group_by

	def get_group_by(self):
		return self.group_by

	def set_order_by(self, order_by):
		self.order_by = order_by

	def get_order_by(self):
		return self.order_by

	def __str__(self):
		return '\n' + str(self.select) + str(self._from) + str(self.join) + str(self.where) + str(self.group_by) + str(self.order_by) + ';\n'

	def print_json(self, filename="output.json"):
		output = open(filename, 'a')
		output.write('{\n')
		self.select.print_json(output)
		self._from.print_json(output)
		self.join.print_json(output)
		self.where.print_json(output)
		self.group_by.print_json(output)
		self.order_by.print_json(output)
		output.write('}\n')
		output.close()
