import os
from PIL import Image, ImageTk
import re
import tkinter
from tkinter import scrolledtext, filedialog, simpledialog

import pandas as pd

# For images to display they need to be global or else they get garbage collected
spectrum_img = ""
fooof_img = ""


class Window:
    images_index = 0
    discarded_data = []
    key_press = 0

    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.title("Data Analysis Swipe")

        self.next_button = tkinter.Button(
            self.window, text="NEXT", command=self.__next_clicked
        )
        self.previous_button = tkinter.Button(
            self.window, text="PREVIOUS", command=self.__previous_clicked
        )
        self.browse_button = tkinter.Button(
            self.window, text="BROWSE", command=self.__browse_clicked
        )
        self.browse_path_entry = tkinter.Entry(self.window, width=63)
        self.browse_path_entry.insert(tkinter.END, "PRESS BROWSE")
        self.discard_scroll_text = scrolledtext.ScrolledText(self.window, height=35)
        self.segment_spectrum_image = tkinter.Label(self.window)
        self.fooof_image = tkinter.Label(self.window)
        self.discard_figure_button = tkinter.Button(
            self.window, text="DISCARD", command=self.__discard_clicked
        )
        self.choose_index_button = tkinter.Button(
            self.window, text="CHOOSE INDEX", command=self.__choose_index_clicked
        )

        self.browse_path_entry.grid(row=0, column=0)
        self.browse_button.grid(row=0, column=1)
        self.discard_figure_button.grid(row=0, column=2)
        self.choose_index_button.grid(row=0, column=3)
        self.previous_button.grid(row=0, column=4)
        self.next_button.grid(row=0, column=5)
        self.fooof_image.grid(row=1, column=0, columnspan=2)
        self.segment_spectrum_image.grid(row=1, column=2, columnspan=2)
        self.discard_scroll_text.grid(row=1, column=4, columnspan=2)

    def __next_clicked(self):
        if self.images_index < len(self.png_keys) - 1:
            self.images_index += 1
            self.__update_figure_shown()
        else:
            print("Cannot view next, all images have been viewed")

    def __previous_clicked(self):
        if self.images_index > 0:
            self.images_index -= 1
            self.__update_figure_shown()
        else:
            print("Cannot view previous, no previous images left")

    def __browse_clicked(self):
        filename = filedialog.askdirectory()
        if os.path.isdir(filename) is False:
            print("The provided path was not a directory.")
            return

        self.browse_path_entry.delete(0, tkinter.END)
        self.browse_path_entry.insert(tkinter.END, filename)

        _segment_spectrum_file_ending = "_segment_spectrum.png"
        _fooof_file_ending = "_FOOOF.png"
        _fooof_file_regex = re.compile(r"(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)(\d)(\d)?")

        files_array = []
        for root, dirs, files in os.walk(filename):
            for png in files:
                if png.endswith(_segment_spectrum_file_ending) or png.endswith(
                    _fooof_file_ending
                ):
                    files_array.append(os.path.join(root, png))

        self.png_paths = {}
        for png_file in files_array:
            png_file_name = _fooof_file_regex.search(png_file)
            if png_file_name is not None:
                if png_file_name[0] not in self.png_paths:
                    self.png_paths[png_file_name[0]] = [png_file]
                else:
                    self.png_paths[png_file_name[0]].append(png_file)
        self.png_keys = list(self.png_paths.keys())
        self.__update_figure_shown()
        self.__update_notes_section()

    def __choose_index_clicked(self):
        index = simpledialog.askinteger(title="Choose Index", prompt="Choose Index")
        if index < 0:
            print("Can't choose a negative integer")
        elif index > len(self.png_keys) - 1:
            print("Can't choose an integer greater than the amount of files available")
        else:
            self.images_index = index
            self.__update_figure_shown()

    def __update_figure_shown(self):
        global fooof_img, spectrum_img
        print(f"{self.images_index} : {len(self.png_keys) - 1}")
        key = self.png_keys[self.images_index]
        _fooof_image_path = self.png_paths[key][0]
        og_image = Image.open(_fooof_image_path)
        rs_image = og_image.resize((600, 600), Image.ANTIALIAS)
        fooof_img = ImageTk.PhotoImage(rs_image)
        self.fooof_image.configure(image=fooof_img)

        _spectrum_image_path = self.png_paths[key][1]
        og_image = Image.open(_spectrum_image_path)
        rs_image = og_image.resize((600, 600), Image.ANTIALIAS)
        spectrum_img = ImageTk.PhotoImage(rs_image)
        self.segment_spectrum_image.configure(image=spectrum_img)

    def __discard_clicked(self):
        self.discarded_data = []
        if os.path.exists("TossData.txt"):
            with open("TossData.txt", "r") as notes:
                for name in notes.read().split("\n"):
                    self.discarded_data.append(name)

        discarded_item = self.png_keys[self.images_index]
        if discarded_item in self.discarded_data:
            self.discarded_data.remove(discarded_item)
        else:
            self.discarded_data.append(discarded_item)

        self.discarded_data = list(filter(None, self.discarded_data))

        with open("TossData.txt", "w") as notes:
            for item in self.discarded_data:
                notes.write(item + "\n")

        self.__update_notes_section()

    def __update_notes_section(self):
        if os.path.exists("TossData.txt"):
            with open("TossData.txt", "r") as notes:
                self.discard_scroll_text.delete("1.0", tkinter.END)
                self.discard_scroll_text.insert(tkinter.END, notes.read())
                self.discard_scroll_text.see(tkinter.END)

    def start_application(self):
        self.window.mainloop()


if __name__ == "__main__":
    global window
    window = Window()
    window.start_application()
