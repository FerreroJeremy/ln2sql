#!/usr/bin/python3
import tkinter.filedialog
from tkinter import *
from tkinter.messagebox import *

from .ln2sql import Ln2sql


class App:
    def __init__(self, root):
        root.title('ln2sql')
        root.bind('<Return>', self.parse)

        self.sentence_frame = LabelFrame(root, text="Input Sentence", padx=5, pady=5)
        self.sentence_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.input_sentence_string = StringVar()
        self.input_sentence_string.set("Enter a sentence...")
        self.input_sentence_entry = Entry(self.sentence_frame, textvariable=self.input_sentence_string, width=50)
        self.input_sentence_entry.pack()
        self.input_sentence_entry.bind('<Button-1>', self.clearEntry)

        self.database_frame = LabelFrame(root, text="Database Selection", padx=5, pady=5)
        self.database_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.database_path_label = Label(self.database_frame, text="No SQL dump selected...")
        self.database_path_label.pack(side="left")

        self.load_database_button = Button(self.database_frame, text="Choose a SQL dump", command=self.find_sql_file,
                                           width=20)
        self.load_database_button.pack(side="right")

        self.language_frame = LabelFrame(root, text="Language Configuration Selection", padx=5, pady=5)
        self.language_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.language_path_label = Label(self.language_frame, text="No configuration file selected...")
        self.language_path_label.pack(side="left")

        self.load_language_button = Button(self.language_frame, text="Choose a configuration file file",
                                           command=self.find_csv_file, width=20)
        self.load_language_button.pack(side="right")

        self.thesaurus_frame = LabelFrame(root, text="Import your personal thesaurus ?", padx=5, pady=5)
        self.thesaurus_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.thesaurus_path_label = Label(self.thesaurus_frame, text="No thesaurus selected...")
        self.thesaurus_path_label.pack(side="left")

        self.load_thesaurus_button = Button(self.thesaurus_frame, text="Choose a thesaurus file",
                                            command=self.find_thesaurus_file, width=20)
        self.load_thesaurus_button.pack(side="right")

        self.go_button = Button(root, text="Go!", command=self.lanch_parsing)
        self.go_button.pack(side="right", fill="both", expand="yes", padx=10, pady=2)

        self.reset_button = Button(root, text="Reset", fg="red", command=self.reset_window)
        self.reset_button.pack(side="right", fill="both", expand="yes", padx=10, pady=2)

    def clearEntry(self, event):
        self.input_sentence_string.set("")

    def parse(self, event):
        self.lanch_parsing()

    def find_sql_file(self):
        filename = tkinter.filedialog.askopenfilename(title="Select a SQL file",
                                                      filetypes=[('sql files', '.sql'), ('all files', '.*')])
        self.database_path_label["text"] = filename

    def find_thesaurus_file(self):
        filename = tkinter.filedialog.askopenfilename(title="Select a thesaurus file",
                                                      filetypes=[('thesaurus files', '.dat'), ('all files', '.*')])
        self.thesaurus_path_label["text"] = filename

    def find_csv_file(self):
        filename = tkinter.filedialog.askopenfilename(title="Select a language configuration file",
                                                      filetypes=[('csv files', '.csv'), ('all files', '.*')])
        self.language_path_label["text"] = filename

    def reset_window(self):
        self.database_path_label["text"] = "No SQL dump selected..."
        self.thesaurus_path_label["text"] = "No thesaurus selected..."
        self.input_sentence_string.set("Enter a sentence...")
        self.language_path_label["text"] = "No configuration file selected..."
        return

    def lanch_parsing(self):
        try:
            thesaurus_path = None

            if str(self.thesaurus_path_label["text"]) != "No thesaurus selected...":
                thesaurus_path = str(self.thesaurus_path_label["text"])

            if (str(self.database_path_label["text"]) != "No SQL dump selected...") and (
                        str(self.language_path_label["text"]) != "No configuration file selected...") and (
                        str(self.input_sentence_string.get()) != "Enter a sentence..."):
                Ln2sql(self.database_path_label["text"], self.input_sentence_string.get(),
                       self.language_path_label["text"], thesaurus_path=thesaurus_path,
                       json_output_path='./output.json')
                showinfo('Result', 'Parsing done!')
            else:
                showwarning('Warning', 'You must fill in all fields, please.')
        except Exception as e:
            showwarning('Error', e)
        return


root = Tk()
App(root)
root.resizable(width=FALSE, height=FALSE)
root.mainloop()
