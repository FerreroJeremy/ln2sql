#!/usr/bin/python
# -*- coding: utf-8 -*

from Tkinter import *
import tkFileDialog
from tkMessageBox import *
from ln2sql import ln2sql

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

class App:
	def __init__(self, root):
		root.title('ln2sql')

		self.sentence_frame = LabelFrame(root, text="Input Sentence", padx=5, pady=5)
		self.sentence_frame.pack(fill="both", expand="yes", padx=10, pady=10)

		self.input_sentence_string = StringVar() 
		self.input_sentence_string.set("Enter a sentence...")
		self.input_sentence_entry = Entry(self.sentence_frame, textvariable=self.input_sentence_string, width=75)
		self.input_sentence_entry.pack()
		self.input_sentence_entry.bind('<Button-1>', self.clearEntry)


		self.database_frame = LabelFrame(root, text="Database Selection", padx=5, pady=5)
		self.database_frame.pack(fill="both", expand="yes", padx=10, pady=10)

		self.database_path_label = Label(self.database_frame, text="No SQL dump selected...")
		self.database_path_label.pack(side="left")

		self.load_database_button = Button(self.database_frame, text="Choose a SQL dump", command=self.find_sql_file, width=20)
		self.load_database_button.pack(side="right")


		self.thesaurus_frame = LabelFrame(root, text="Import your personal thesaurus ?", padx=5, pady=5)
		self.thesaurus_frame.pack(fill="both", expand="yes", padx=10, pady=10)

		self.thesaurus_path_label = Label(self.thesaurus_frame, text="No thesaurus selected...")
		self.thesaurus_path_label.pack(side="left")

		self.load_thesaurus_button = Button(self.thesaurus_frame, text="Choose a thesaurus file", command=self.find_thesaurus_file, width=20)
		self.load_thesaurus_button.pack(side="right")


		settings_frame = Frame(root, padx=5, pady=5)
		settings_frame.pack(fill="both", expand="yes")


		self.language_frame = LabelFrame(settings_frame, text="Language Selection", padx=5, pady=5)
		self.language_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5)


		self.language = StringVar()
		self.language.set("english")
		self.english_radio_button = Radiobutton(self.language_frame, text="English", variable=self.language, value="english", justify="left")
		self.french_radio_button = Radiobutton(self.language_frame, text="French", variable=self.language, value="french", justify="left")
		self.spanish_radio_button = Radiobutton(self.language_frame, text="Spanish", variable=self.language, value="spanish", justify="left")
		self.italian_radio_button = Radiobutton(self.language_frame, text="Italian", variable=self.language, value="italian", justify="left")
		self.german_radio_button = Radiobutton(self.language_frame, text="German", variable=self.language, value="german", justify="left")
		self.english_radio_button.pack(side="top", fill="both", expand="yes")
		self.french_radio_button.pack(side="top", fill="both", expand="yes")
		self.spanish_radio_button.pack(side="top", fill="both", expand="yes")
		self.italian_radio_button.pack(side="top", fill="both", expand="yes")
		self.german_radio_button.pack(side="top", fill="both", expand="yes")


		self.output_frame = LabelFrame(settings_frame, text="Output Settings", padx=5, pady=5)
		self.output_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5)

		self.translate_sql_value = IntVar()
		self.translate_no_sql_value = IntVar()
		self.json_output_value = IntVar()
		self.translate_sql_button = Checkbutton(self.output_frame, text="Translate to SQL query", variable=self.translate_sql_value, justify="left")
		self.translate_no_sql_button = Checkbutton(self.output_frame, text="Translate to NoSQL query", variable=self.translate_no_sql_value, justify="left")
		self.print_json_file_button = Checkbutton(self.output_frame, text="Print the query structure in output JSON file", variable=self.json_output_value, justify="left")
		self.translate_sql_button.pack(side="top", fill="both", expand="yes")
		self.translate_no_sql_button.pack(side="top", fill="both", expand="yes")
		self.print_json_file_button.pack(side="top", fill="both", expand="yes")
		self.print_json_file_button.select()
		self.translate_sql_button.select()


		self.go_button = Button(root, text="Go!", command=self.lanch_parsing, width=75)
		self.go_button.pack(padx=5, pady=5)

		self.reset_button = Button(root, text="Reset", fg="red", command=self.reset_window, width=75)
		self.reset_button.pack(padx=5, pady=5)

	def clearEntry(self, event):
		self.input_sentence_string.set("")

	def find_sql_file(self):
		filename = tkFileDialog.askopenfilename(title="Select a SQL file",filetypes=[('sql files','.sql'),('all files','.*')])
		self.database_path_label["text"] = filename

	def find_thesaurus_file(self):
		filename = tkFileDialog.askopenfilename(title="Select a thesaurus file",filetypes=[('thesaurus files','.dat'),('all files','.*')])
		self.thesaurus_path_label["text"] = filename

	def reset_window(self):
		self.database_path_label["text"] = "No SQL dump selected..."
		self.thesaurus_path_label["text"] = "No thesaurus selected..."
		self.input_sentence_string.set("Enter a sentence...")
		self.language.set("english")
		self.print_json_file_button.deselect()
		self.translate_no_sql_button.deselect()
		self.translate_sql_button.deselect()
		return

	def lanch_parsing(self):
		try:
			thesaurus_use = False

			if self.json_output_value.get() == 1:
				json_output_path = './output.json'
			else:
				json_output_path = None

			if str(self.thesaurus_path_label["text"]) != "No thesaurus selected...":
				thesaurus_use = True

			if str(self.database_path_label["text"]) != "No SQL dump selected..." and str(self.input_sentence_string.get()) != "Enter a sentence...":
				ln2sql(self.database_path_label["text"], self.input_sentence_string.get(), str(self.language.get()).lower(), thesaurus_use, json_output_path)
				showinfo('Result', 'Parsing done!')
			else:
				showwarning('Warning','You must fill in all fields, please.')
		except Exception, e:
			showwarning('Error', e)
		return

root = Tk()
App(root)
root.resizable(width=FALSE, height=FALSE)
root.mainloop()