from tkinter import *

wn = Tk()
wn.title('KeyDetect')
m = 0
def down(e):
    global m
    if m == 0:
        print ('Down \n' + e.char)
        m = 1
def up(e):
    global m
    if m == 1:
        print ('Up \n'+ e.char)
        m = 0
wn.bind('<KeyPress>', down)
wn.bind('<KeyRelease>', up)

wn.mainloop()
