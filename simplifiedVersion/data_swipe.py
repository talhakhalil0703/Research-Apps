import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from PIL import ImageTk, Image
import sys
import os
import re

global_index = 0
global_max_index = None
global_files_array_with_location = []
global_png_files_names_to_write = []
global_img = None
key_press = 0
notes_path = 'discard.txt'
file_name_ending_with = '_segment_spectrum.png'
image_size = 600
fooof_file_regex = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)(\d)(\d)?')
data_path_path = ''

def find_files_in_directory(data_path_path):
    global global_files_array_with_location, global_png_files_names_to_write, global_max_index

    files_array = []
    for root, dirs, files in os.walk(data_path_path):
        for png in files:
            if png.endswith(file_name_ending_with):
                files_array.append(os.path.join(root, png))

    png_files_names = []
    for png_file in files_array:
        png_file_name = fooof_file_regex.search(png_file)
        if png_file_name is not None and png_file_name not in png_files_names:
            png_files_names.append(png_file_name[0])

    global_max_index = len(png_files_names)
    print(global_max_index)
    global_files_array_with_location, global_png_files_names_to_write = files_array, png_files_names

def write_to_notes_file(content_to_write):
    with open(notes_path,'a') as notes_to_write:
        notes_to_write.write(content_to_write + '\n')
    read_notes_file()
def read_notes_file():
    with open(notes_path, 'r') as notes_to_read:
        console.delete('1.0' , END)
        console.insert(END, notes_to_read.read())
        console.see(tk.END)
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
    read_notes_file()
def yes_clicked():
    global global_index
    global_index += 1
    update_image_shown()
def no_clicked():
    global global_index, global_png_files_names_to_write
    write_to_notes_file(global_png_files_names_to_write[global_index])
    global_index += 1
    update_image_shown()
def undo_clicked():
    global global_index
    if global_index is 0:
        return
    remove_last_line()
    global_index -= 1
    update_image_shown()

def go_back_one():
    global global_index
    if global_index is 0:
        return
    global_index -= 1
    update_image_shown()
def clear_file():
    global global_index
    global_index = 0
    print('File Cleared')
    print(global_index)
    with open(notes_path, 'w') as notes_to_write:
        notes_to_write.write('')
    read_notes_file()
    update_image_shown()

def find_files_clicked():
    find_files_in_directory(data_path.get())
    update_image_shown()
def exit_clicked():
    sys.exit(0)
def update_index_value_clicked():
    global global_index, global_png_files_names_to_write
    with open(notes_path, 'r') as notes_to_read:
        content = notes_to_read.readlines()
        content[-1] = content[-1].replace('\n', '')
        global_index = global_png_files_names_to_write.index(content[-1])
        print(global_index)

def key_down(key):
    global key_press
    if key_press is 0:
        key_press = 1
def key_up(key):
    global key_press
    if key_press is 1:
        if key.char == 'q':
            exit_clicked()
        if key.char == ',':
            no_clicked()
        if key.char == '.':
            yes_clicked()
        if key.char == 'u':
            undo_clicked()
        if key.char == 'z':
            go_back_one()
        if key.char == '`':
            clear_file()
        key_press = 0

def update_image_shown():
    global global_index, global_files_array_with_location
    print(global_index)
    og_image = Image.open(global_files_array_with_location[global_index])
    rs_image = og_image.resize((image_size,image_size), Image.ANTIALIAS)
    global global_img, exit_button
    global_img = ImageTk.PhotoImage(rs_image)
    global_image.configure(image = global_img)


window = tk.Tk()
window.title('Data Swipe')

yes_button = Button(window, text = 'KEEP FILE', command = yes_clicked)
no_button = Button(window, text = "DISCARD", command = no_clicked)
data_path = Entry(window, width =63)
yes_button.grid(row = 0, column = 0)
no_button.grid(row = 0, column = 1)
data_path.grid(row = 0, column = 2, columnspan = 2)
data_path.insert(END, data_path_path)

console = scrolledtext.ScrolledText(window, height = 35)
global_image = tk.Label(window, image = global_img)
console.grid(row = 1, columnspan = 2, column = 2)
global_image.grid(row = 1, column = 0, columnspan = 2)

find_files_button = Button(window, text = 'FIND FILES', command = find_files_clicked)
exit_button = Button(window, text = 'EXIT', fg = 'red', command = exit_clicked)
update_index_value = Button(window, text = 'UPDATED INDEX', command = update_index_value_clicked)
undo_button = Button(window, text = 'UNDO', command = undo_clicked)

exit_button.grid(row = 2, column = 0)
find_files_button.grid(row = 2, column = 1)
update_index_value.grid(row = 2, column = 2)
undo_button.grid(row = 2, column = 3)

window.bind('<KeyPress>', key_down)
window.bind('<KeyRelease>', key_up)

def data_swipe(data_path_path):
    data_path.insert(END, data_path_path)
    window.mainloop()
