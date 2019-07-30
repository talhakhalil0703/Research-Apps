import tkinter as tk
from tkinter import *
from tkinter import filedialog
import sys
import os

window = tk.Tk()
window.title('Slice Excel Files Into Individual Paitents')
data_path = Entry(window, width =45)
data_path.grid(row = 0, column = 0)
data_path.insert(END, '')

def slice_excel():
    pass
def browse_clicked():
    window.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("excel spreadsheets","*.xlsx"),("all files","*.*")))
    data_path.insert(END, window.filename)
    print(window.filename)
def exit_clicked():
    sys.exit(0)
def run_clicked():
    slice_excel() #doing some function with the excel files and then proceeding to save them

browse_button = Button(window, text = 'BROWSE', command = browse_clicked)
exit_button = Button(window, text = 'EXIT', command = exit_clicked)
run_button = Button(window, text = 'RUN', command = run_clicked)

exit_button.grid(row = 1, column = 0)
browse_button.grid(row = 0, column = 1)
run_button.grid(row = 1, column = 1)

window.mainloop()
