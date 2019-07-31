#Clinic Program for FootHills Talha Khalil
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import sys
import os
import pandas as pd
from openpyxl import load_workbook
import openpyxl
import pyexcel as p

window = tk.Tk()
window.title('Slice Excel Files Into Individual Paitents')
data_path = Entry(window, width = 45)
data_path.grid(row = 0, column = 0)
data_path.insert(END, '')

def slice_excel():
    data_path_string = data_path.get()
    if data_path_string[-4:] != '.xls' and data_path_string[-5:] != '.xlsx':
        print('Wrong file type!')
        return
    if data_path_string[-4:] == '.xls':
        p.save_book_as(file_name= data_path_string, dest_file_name= data_path_string[:-4] + '.xlsx')
        data_path_string = data_path_string[:-4] + '.xlsx'
    df = pd.read_excel(data_path_string)
    df.columns = ['Patient', 'Event Name', 'Date and Time', 'Subtotal score A', 'Subtotal score B','Subtotal score C', 'Total Score']
    df = df.drop([0], axis = 0)
    xls_index = data_path_string.index('.xls')
    path = data_path_string[:xls_index] + ' Individual' + data_path_string[xls_index:]
    wb = openpyxl.Workbook()
    wb.save(path)
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    writer.book = book
    grouped = df.groupby('Patient')
    for patient in grouped.groups:
        new_group = grouped.get_group(patient).T
        new_group.to_excel(writer, sheet_name= str(patient), header = False)
    print('Done')
    writer.save()
    writer.close()

def browse_clicked():
    window.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"), ("Excel spreadsheets","*.xls"),("Excel spreadsheets MAC","*.xlsx")))
    data_path.delete(0, END)
    data_path.insert(END, window.filename)
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
