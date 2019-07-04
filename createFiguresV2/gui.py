import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from exData import exData
import sys
window = tk.Tk()
window.title('Data Extracter')

dataPathText = Label(window, text = 'Data Path: ')
dataPathText.grid(column = 0, row = 0)
dataPath = Entry(window, width =63)
dataPath.grid(column = 1, row = 0, columnspan = 3)
dataPath.insert(END, '/Users/talhakhalil/Desktop/Research/Data')
R2Text = Label(window, text = 'R2 Tolerance: ')
R2Text.grid(column = 0, row = 1)
R2 = Entry(window, width =63)
R2.grid(column = 1, row = 1, columnspan = 3)
R2.insert(END, '0.95')
PeakText = Label(window, text = "Peaks' Bin: ")
PeakText.grid(column = 0, row = 2)
Peak1 = Entry(window)
Peak1.grid(column = 1, row = 2)
Peak2 = Entry(window)
Peak2.grid(column = 2, row = 2)
Peak3 = Entry(window)
Peak3.grid(column = 3, row = 2)
Peak1.insert(END, '0')
Peak2.insert(END, '60')
Peak3.insert(END, '2.5')
AreaText = Label(window, text = 'Area Bins: ')
AreaText.grid(column = 0, row = 3)
Area1 = Entry(window)
Area1.grid(column = 1, row = 3)
Area2 = Entry(window)
Area2.grid(column = 2, row = 3)
Area3 = Entry(window)
Area3.grid(column = 3, row = 3)
Area1.insert(END, '0')
Area2.insert(END, '10')
Area3.insert(END, '1')

AlphaText = Label(window, text = 'Points alpha value: ')
Alpha = Entry(window, width =63)
Alpha.grid(column = 1, row = 4, columnspan = 3)
Alpha.insert(END, '0.2')
AlphaText.grid(column = 0, row = 5)
mmToChooseText = Label(window, text = 'How many mm do you want? : ')
mmToChoose = Entry(window, width =63)
mmToChoose.grid(column = 1, row = 5, columnspan = 3)
mmToChoose.insert(END, '0.2')
mmToChooseText.grid(column = 0, row = 5)

def runClicked():
	PeakArray = [float(Peak1.get()), float(Peak2.get()), float(Peak3.get())]
	AreaArray = [float(Area1.get()), float(Area2.get()), float(Area3.get())]
	exData(dataPath.get(), R2.get(), PeakArray, AreaArray, Alpha.get(), mmToChoose.get())

def exitClicked():
	sys.exit(0)

RunButton = Button(window, text = 'Run', command = runClicked)
RunButton.grid(row = 7, column = 1)
ExitButton = Button(window, text = 'Exit', command = exitClicked)
ExitButton.grid(row = 7, column = 2)
Console = scrolledtext.ScrolledText(window, height=10)
Console.grid(row = 6,columnspan = 4)

def redirector(inputStr):
    Console.insert(INSERT, inputStr)

sys.stdout.write = redirector
window.mainloop()
