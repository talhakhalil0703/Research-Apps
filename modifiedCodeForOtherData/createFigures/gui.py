import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from main import main
import sys

window = tk.Tk()
window.title('Data Extracter')

data_path_text = Label(window, text = 'Data Path: ')
data_path_text.grid(column = 0, row = 0)
data_path = Entry(window, width =63)
data_path.grid(column = 1, row = 0, columnspan = 3)
data_path.insert(END, '/Users/talhakhalil/Desktop/OtherData')
r2_text = Label(window, text = 'R2 Tolerance: ')
r2_text.grid(column = 0, row = 1)
r2 = Entry(window, width =63)
r2.grid(column = 1, row = 1, columnspan = 3)
r2.insert(END, '0.95')
peak_text = Label(window, text = "Peaks' Bin: ")
peak_text.grid(column = 0, row = 2)
peak_1 = Entry(window)
peak_1.grid(column = 1, row = 2)
peak_2 = Entry(window)
peak_2.grid(column = 2, row = 2)
peak_3 = Entry(window)
peak_3.grid(column = 3, row = 2)
peak_1.insert(END, '0')
peak_2.insert(END, '60')
peak_3.insert(END, '2.5')
area_text = Label(window, text = 'Area Bins: ')
area_text.grid(column = 0, row = 3)
area_1 = Entry(window)
area_1.grid(column = 1, row = 3)
area_2 = Entry(window)
area_2.grid(column = 2, row = 3)
area_3 = Entry(window)
area_3.grid(column = 3, row = 3)
area_1.insert(END, '0')
area_2.insert(END, '10')
area_3.insert(END, '1')

alpha_text = Label(window, text = 'Points alpha value: ')
alpha = Entry(window, width =63)
alpha.grid(column = 1, row = 4, columnspan = 3)
alpha.insert(END, '0.2')
alpha_text.grid(column = 0, row = 4)

def run_clicked():
	peak_Array = [float(peak_1.get()), float(peak_2.get()), float(peak_3.get())]
	area_Array = [float(area_1.get()), float(area_2.get()), float(area_3.get())]
	main(data_path.get(), r2.get(), peak_Array, area_Array, alpha.get())

def exit_clicked():
	sys.exit(0)

run_button = Button(window, text = 'Run', command = run_clicked)
run_button.grid(row = 7, column = 1)
exit_button = Button(window, text = 'Exit', command = exit_clicked)
exit_button.grid(row = 7, column = 2)

window.mainloop()
