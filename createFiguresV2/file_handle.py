import os
import re

file_name_result = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')
file_name = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?')


def find_file_directory(data_path):

    file_directory = []
    for root, dirs, files in os.walk(data_path):
        for mm_file in files:
            if mm_file.endswith('_fooof_results.mat'):
                file_directory.append(os.path.join(root, mm_file))

    return file_directory


def find_files(data_path, directory, search_for_mm):
    files_array = []
    for x in directory:
        name = file_name_result.search(x) if search_for_mm else name = file_name.search(x)
        if name is not None and name not in files_array:
            files_array.append(name[0])
        files_array.sort()
    return files_array


def remove_files(results_list, remove_list):

    for x in remove_list:
        name = file_name_result.search(x)
        if name[3] is None:
            for y in results_list:
                remove = file_name.search(y)
                if x == remove[0]:
                     results_list.remove(y)
        else:
            try:
                results_list.remove(x)
            except:
                continue
    return results_list


def read_file_names(file_path):
    find_file_names =[]

    with open(file_path, 'r') as file_to_read
        file_content = file_to_read.read()

    to_add = file_name_result.findall(file_content)

    for x in to_add:
        y = x[0] + x[1] + x[2] + x[3] + x[4]
        find_file_names.append(y)

    find_file_names.sort()
    return find_file_names
