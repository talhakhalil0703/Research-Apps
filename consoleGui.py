import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from exData import exData
import sys
 

class RedirectText(object):

    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.insert(tk.END, string)
 
class MyApp(object):

    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Data Extracter")
        self.dataPathText = Label(self.root, text = 'Data Path: ')
        self.dataPathText.grid(column = 0, row = 0)
        self.dataPath = Entry(self.root, width =63)
        self.dataPath.grid(column = 1, row = 0, columnspan = 3)
        self.dataPath.insert(END, '/Users/talhakhalil/Desktop/Research/Data')
        self.R2Text = Label(self.root, text = 'R2 Tolerance: ')
        self.R2Text.grid(column = 0, row = 1)
        self.R2 = Entry(self.root, width =63)
        self.R2.grid(column = 1, row = 1, columnspan = 3)
        self.R2.insert(END, '0.95')
        self.PeakText = Label(self.root, text = "Peaks' Bin: ")
        self.PeakText.grid(column = 0, row = 2)
        self.Peak1 = Entry(self.root)
        self.Peak1.grid(column = 1, row = 2)
        self.Peak2 = Entry(self.root)
        self.Peak2.grid(column = 2, row = 2)
        self.Peak3 = Entry(self.root)
        self.Peak3.grid(column = 3, row = 2)
        self.Peak1.insert(END, '0')
        self.Peak2.insert(END, '60')
        self.Peak3.insert(END, '2.5')
        self.AreaText = Label(self.root, text = 'Area Bins: ')
        self.AreaText.grid(column = 0, row = 3)
        self.Area1 = Entry(self.root)
        self.Area1.grid(column = 1, row = 3)
        self.Area2 = Entry(self.root)
        self.Area2.grid(column = 2, row = 3)
        self.Area3 = Entry(self.root)
        self.Area3.grid(column = 3, row = 3)
        self.Area1.insert(END, '0')
        self.Area2.insert(END, '10')
        self.Area3.insert(END, '1')

        self.AlphaText = Label(self.root, text = 'Points alpha value: ')
        self.Alpha = Entry(self.root, width =63)
        self.Alpha.grid(column = 1, row = 4, columnspan = 3)
        self.Alpha.insert(END, '0.2')
        self.AlphaText.grid(column = 0, row = 4)

        def runClicked():
            self.PeakArray = [float(self.Peak1.get()), float(self.Peak2.get()), float(self.Peak3.get())]
            self.AreaArray = [float(self.Area1.get()), float(self.Area2.get()), float(self.Area3.get())]
            exData(self.dataPath.get(), self.R2.get(), self.PeakArray, self.AreaArray, self.Alpha.get())

        def exitClicked():
            sys.exit(0)

        self.RunButton = Button(self.root, text = 'Run', command = runClicked)
        self.RunButton.grid(row = 6, column = 1)
        self.ExitButton = Button(self.root, text = 'Exit', command = exitClicked)
        self.ExitButton.grid(row = 6, column = 2)
        self.Console = scrolledtext.ScrolledText(self.root, height=10)
        self.Console.grid(row = 5,columnspan = 4)
        # redirect stdout
        redir = RedirectText(self.Console)
        sys.stdout = redir

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()