# -*- coding: utf-8 -*

import os
import time

class Select():
	count = False
	columns = []

	def __init__(self, count=None, columns=None):
		if count is not None:
			self.count = count
		if columns is not None:
			self.columns = columns

	def set_count_type(self, count):
		self.count = count

	def add_column(self, column):
		self.columns.append(column)

	def print_me(self, output):
		if len(self.columns) >= 1:
			if len(self.columns) == 1:
				output.write('\t"select": {\n')
				output.write('\t\t"count": "' + str(self.count) + '",\n')
				output.write('\t\t"column": "' + str(self.columns[0]) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"select": {\n')
				output.write('\t\t"count": "' + str(self.count) + '",\n')
				output.write('\t\t"columns": [')
				for i in range(0, len(self.columns)):
					if i == (len(self.columns)-1):
						output.write('"' + str(self.columns[i]) + '"')
					else:
						output.write('"' + str(self.columns[i]) + '", ')
				output.write(']\n')
				output.write('\t},\n')

class From():
	table = ''

	def __init__(self, table=None):
		if table is not None:
			self.table = table

	def set_table(self, table):
		self.table = table

	def print_me(self, output):
		output.write('\t"from": {\n')
		output.write('\t\t"table": "' + str(self.table) + '"\n')
		output.write('\t},\n')

class Join():
	tables = []

	def __init__(self, tables=None):
		if tables is not None:
			self.tables = tables

	def add_table(self, table):
		self.tables.append(table)

	def print_me(self, output):
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

class Condition():
	column = ''
	operator = ''
	value = ''

	def __init__(self, column, operator, value):
		self.column = column
		self.operator = operator
		self.value = value

	def print_me(self, output):
		output.write('\t\t\t{ "column": "' + str(self.column) + '",\n\t\t\t  "operator": "' + str(self.operator) + '",\n\t\t\t  "value": "' + str(self.value) + '"\n\t\t\t}')

class Where():
	conditions = []

	def __init__(self, clause):
		self.conditions.append([None, clause])

	def add_condition(self, junction, clause):
		self.conditions.append([junction, clause])

	def print_me(self, output):
		if len(self.conditions) >= 1:
			if len(self.conditions) == 1:
				output.write('\t"where": {\n')
				output.write('\t\t"condition": [\n')
				self.conditions[0][1].print_me(output)
				output.write('\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
			else:
				output.write('\t"where": {\n')
				output.write('\t\t"conditions": [\n')
				for i in range(0, len(self.conditions)):
					if self.conditions[i][0] is not None:
						output.write('\t\t\t{ "operator": "' + str(self.conditions[i][0]) + '" },\n')
					self.conditions[i][1].print_me(output)
					if i != (len(self.conditions)-1):
						output.write(',')
					output.write('\n')
				output.write('\t\t]\n')
				output.write('\t},\n')
    
class GroupBy():
	columns = []

	def __init__(self, columns=None):
		if columns is not None:
			self.columns = columns

	def add_column(self, column):
		self.columns.append(column)

	def print_me(self, output):
		if len(self.columns) >= 1:
			if len(self.columns) == 1:
				output.write('\t"group_by": {\n')
				output.write('\t\t"column": "' + str(self.columns[0]) + '"\n')
				output.write('\t},\n')
			else:
				output.write('\t"group_by": {\n')
				output.write('\t\t"columns": [')
				for i in range(0, len(self.columns)):
					if i == (len(self.columns)-1):
						output.write('"' + str(self.columns[i]) + '"')
					else:
						output.write('"' + str(self.columns[i]) + '", ')
				output.write(']\n')
				output.write('\t},\n')

class OrderBy():
	column = ''
	order = None

	def __init__(self, column=None, order=None):
		if column is not None:
			self.column = column
		if order is not None:
			self.order = order

	def add_order(self, column, order):
		self.column = column
		self.order = order

	def print_me(self, output):
		output.write('\t"order_by": {\n')
		output.write('\t\t"order": "' + str(self.order) + '",\n')
		output.write('\t\t"column": "' + str(self.column) + '"\n')
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
		if _from is not None:
			self._from = _from
		if join is not None:
			self.join = join
		if where is not None:
			self.where = where
		if group_by is not None:
			self.group_by = group_by
		if order_by is not None:
			self.order_by = order_by

	def set_select(self, select):
		self.select = select

	def set_from(self, _from):
		self._from = _from

	def set_join(self, join):
		self.join = join

	def set_where(self, where):
		self.where = where

	def set_group_by(self, group_by):
		self.group_by = group_by

	def set_order_by(self, order_by):
		self.order_by = order_by

	def print_me(self, filename="output.json"):
		if os.path.exists(filename):
			os.remove(filename)

		output = open(filename, 'a')
		output.write('{\n')
		if self.select is not None:
			self.select.print_me(output)
		if self._from is not None:
			self._from.print_me(output)
		if self.join is not None:
			self.join.print_me(output)
		if self.where is not None:
			self.where.print_me(output)
		if self.group_by is not None:
			self.group_by.print_me(output)
		if self.order_by is not None:
			self.order_by.print_me(output)
		output.write('}\n')
		output.close()



