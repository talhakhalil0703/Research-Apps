import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import sys
import os
import re

window = tk.Tk()
window.title('Note Creator')

notes_content = ''
notes_path = 'notes.txt'
content_to_write = 'zxczxc'

old_time_name = ''
patient_number = ''
time_start = ''
time_end = ''
mm_start = ''
mm_end = ''
type_of_test = ''

patient_number_text = Label(window, text = 'Patient Number:')
time_start_text = Label(window, text = 'Time Start:')
time_end_text = Label(window, text = 'Time End:')
mm_start_text = Label(window, text = 'MM Start:')
mm_end_text = Label(window, text = 'MM End:')
type_of_test_text = Label(window, text = 'Comment:')

patient_number_text_box= Entry(window)
time_start_text_box = Entry(window)
time_end_text_box = Entry(window)
mm_start_text_box = Entry(window)
mm_end_text_box = Entry(window)
type_of_test_text_box = Entry(window)
patient_number_text_box.insert(END, patient_number)
time_start_text_box.insert(END, time_start)
time_end_text_box.insert(END, time_end)
mm_start_text_box.insert(END, mm_start)
mm_end_text_box.insert(END, mm_end)
type_of_test_text_box.insert(END, type_of_test)

patient_number_text.grid(column = 0, row = 0)
time_start_text.grid(column = 2, row = 0)
time_end_text.grid(column = 4, row = 0)
mm_start_text.grid(column = 2, row = 1)
mm_end_text.grid(column = 4, row = 1)
type_of_test_text.grid(column = 0, row = 1)
patient_number_text_box.grid(column = 1, row = 0)
time_start_text_box.grid(column = 3, row = 0)
time_end_text_box.grid(column = 5, row = 0)
mm_start_text_box.grid(column = 3, row = 1)
mm_end_text_box.grid(column = 5, row = 1)
type_of_test_text_box.grid(column = 1, row = 1)

console = scrolledtext.ScrolledText(window, height = 35)
console.grid(column = 0, columnspan = 6, row = 3)

time_regex = re.compile(r'(\d\d)(:)(\d\d)(:)(\d\d)')

def read_notes_file():
    with open(notes_path, 'r') as notes_to_read:
        console.delete('1.0' , END)
        console.insert(END, notes_to_read.read())
        console.see(tk.END)

def write_to_notes_file(content_to_write):
    with open(notes_path,'a') as notes_to_write:
        notes_to_write.write(content_to_write)

def remove_last_line():
    content = ''
    with open(notes_path, 'r') as notes_to_read:
        content = notes_to_read.readlines()
        content.pop(-1)
    with open(notes_path, 'w') as notes_to_write:
        replace_content = ''
        for line in content:
            replace_content += line
        notes_to_write.write(replace_content)

def next_values():
    return patient_number_text_box.get(), time_end_text_box.get(), ' ', mm_end_text_box.get(), ' ', ' '

def insert_values(patient_number, time_start, time_end, mm_start, mm_end, type_of_test):
    patient_number_text_box.delete(0 , END)
    time_start_text_box.delete(0, END)
    time_end_text_box.delete(0 , END)
    mm_start_text_box.delete(0 , END)
    mm_end_text_box.delete(0 , END)
    type_of_test_text_box.delete(0 , END)
    patient_number_text_box.insert(END, patient_number)
    time_start_text_box.insert(END, time_start)
    time_end_text_box.insert(END, time_end)
    mm_start_text_box.insert(END, mm_start)
    mm_end_text_box.insert(END, mm_end)
    type_of_test_text_box.insert(END, type_of_test)

def generate_string():
    time_name = ''
    if time_start_text_box.get() != '':
        global old_time_name
        time_name = time_regex.search(time_start_text_box.get())
        time_name = time_name[1] + time_name[3]
        if time_name == old_time_name:
            time_name += 'B'
        old_time_name = time_name
    return patient_number_text_box.get() + '-' + time_name + '  ' + time_start_text_box.get() + '  ' + time_end_text_box.get() + '  ' + mm_start_text_box.get() + ' to ' + mm_end_text_box.get() + '  ' + type_of_test_text_box.get() + '\n'

def exit_clicked():
    sys.exit(0)

def write_clicked():
    write_to_notes_file(generate_string())
    patient_number, time_start, time_end, mm_start, mm_end, type_of_test = next_values()
    insert_values(patient_number, time_start, time_end, mm_start, mm_end, type_of_test)
    read_notes_file()

def comment_button_clicked():
    write_to_notes_file(type_of_test_text_box.get())
    write_to_notes_file('\n')
    insert_values('','','','','','')
    read_notes_file()
def next_trajectory_clicked():
    insert_values('','','','','','')
    read_notes_file()

def remove_last_clicked():
    remove_last_line()
    read_notes_file()

def read_button_clicked():
    read_notes_file()

exit_button = Button(window, text = 'Exit', command = exit_clicked)
write_button = Button(window, text = 'Write', command = write_clicked)
remove_last_button = Button(window, text = 'Remove Last', command = remove_last_clicked)
next_trajectory = Button(window, text = 'Next Trajectory', command = next_trajectory_clicked)
read_button = Button(window, text = 'Print File', command = read_button_clicked)
comment_button = Button(window, text= 'Just Comment', command = comment_button_clicked)
exit_button.grid(column = 0, row = 2)
comment_button.grid(column = 1, row = 2)
write_button.grid(column = 2, row = 2)
remove_last_button.grid(column = 3, row = 2)
next_trajectory.grid(column = 4, row = 2)
read_button.grid(column = 5, row = 2)

window.mainloop()
