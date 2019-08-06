#Clinic Program for FootHills Talha Khalil
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import sys
import os
from openpyxl import load_workbook
import openpyxl
import pyexcel as p
import pandas as pd

window = tk.Tk()
window.title('Slice Excel Files Into Individual Paitents')
data_path = Entry(window, width = 45)
data_path.grid(row = 0, column = 0)
data_path.insert(END, '')

def slice_excel():
    data_path_string = data_path.get()

    if data_path_string[-4:] != '.xls' and data_path_string[-5:] != '.xlsx': #Checking to see if its an excel file
        print('Wrong file type!')
        return

    if data_path_string[-4:] == '.xls': #If its the xls format convert to xlsx format as that is newer and works better
        p.save_book_as(file_name= data_path_string, dest_file_name= data_path_string[:-4] + '.xlsx')
        data_path_string = data_path_string[:-4] + '.xlsx'

    df = pd.read_excel(data_path_string)
    #At the point you could check what type of dataset you're reading, however I only have one right now so don't need to check for it
    df.columns = ['Patient', 'Event Name', 'Date and Time', 'Subtotal score A', 'Subtotal score B','Subtotal score C', 'Total Score']
    #Changed the names of the headers as they are originally mismatched
    df = df.drop([0], axis = 0) #removing the actual header that is put in the wrong row

    #Creating a name for the result file by modifing the original name slightly
    xls_index = data_path_string.index('.xls')
    path = data_path_string[:xls_index] + ' Individual' + data_path_string[xls_index:]

    #Opening the workbook
    wb = openpyxl.Workbook()
    wb.save(path)
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    writer.book = book
    grouped = df.groupby('Patient')

    #Splicing the data into patients and transposing it so its easier to read
    for patient in grouped.groups:
        new_group = grouped.get_group(patient).T
        new_group.to_excel(writer, sheet_name= str(patient), header = False)
        current_sheet = writer.sheets[str(patient)]
        current_sheet.column_dimensions['A'].width = 17
        current_sheet.column_dimensions['B'].width = 18
        current_sheet.column_dimensions['C'].width = 33
        current_sheet.column_dimensions['D'].width = 31

    #Saving
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
    slice_excel()

browse_button = Button(window, text = 'BROWSE', command = browse_clicked)
exit_button = Button(window, text = 'EXIT', command = exit_clicked)
run_button = Button(window, text = 'RUN', command = run_clicked)

exit_button.grid(row = 1, column = 0)
browse_button.grid(row = 0, column = 1)
run_button.grid(row = 1, column = 1)
window.mainloop()
