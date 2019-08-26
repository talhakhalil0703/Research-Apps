from tkinter import *
from tkinter import filedialog
import sys

from create_fooof import create_fooof_main
from extract_fooof import extract_fooof_main
from data_swipe import data_swipe

root = Tk()
root.title('Fooof Automation')

def create_fooof_button_clicked():
    create_fooof_main(data_path.get())

def extract_fooof_button_clicked():
    extract_fooof_main(data_path.get())

def data_swipe_button_clicked():
    data_swipe(data_path.get())

def browse_clicked():
    root.filename = filedialog.askdirectory()
    data_path.delete(0, END)
    data_path.insert(END, root.filename)

data_path = Entry(root, width = 45)
data_path.grid(row = 0, column = 0, columnspan = 2)
data_path.insert(END, '')

browse_button = Button(root, text = 'BROWSE', command = browse_clicked)
browse_button.grid(row = 0, column = 2)

create_fooof_button = Button(root, text = 'CREATE FOOOF FILES', command = create_fooof_button_clicked)
create_fooof_button.grid(row = 1, column = 0, padx = (20,20))

data_swipe_button = Button(root, text = 'DATA SWIPE', command = data_swipe_button_clicked)
data_swipe_button.grid(row = 1, column = 1, padx = (20,20))

extract_fooof_button = Button(root, text = 'EXTRACT FOOOF FILES INTO EXCEL', command = extract_fooof_button_clicked)
extract_fooof_button.grid(row = 1, column = 2, padx = (20,20))

root.mainloop()
