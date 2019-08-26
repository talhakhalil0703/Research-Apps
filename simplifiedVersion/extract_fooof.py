import time
import numpy
import openpyxl
import matlab.engine
import re
import os
import scipy.io as sio

patient_number = re.compile(r'(\d\d\d\d)(-)')
individual_file_name = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')

class SegmentFile:
    def __init__(self, name):
        self.name = name
        self.exponent = None
        self.offset = None
        self.r2 = None
        self.error = None
        self.peak_freq = []
        self.freq_area = []

def read_file_names(file_path):
    find_file_names =[]
    with open(file_path, 'r') as file_to_read:
        file_content = file_to_read.read()
    to_add = individual_file_name.findall(file_content)
    for x in to_add:
        y = x[0] + x[1] + x[2] + x[3] + x[4]
        find_file_names.append(y)

    find_file_names.sort()
    return find_file_names

def find_file_directory(data_path):
    file_directory = []
    for root, dirs, files in os.walk(data_path):
        for mm_file in files:
            if mm_file.endswith('_fooof_results.mat'):
                file_directory.append(os.path.join(root, mm_file))
    file_directory.sort()
    return file_directory

def extract_single_file_data(file_name):
    file_content = sio.loadmat(file_name)
    struct = file_content['fooof_results']
    temp_file = SegmentFile(individual_file_name.search(file_name)[0])
    val = struct[0,0]
    temp_file.exponent = val['background_params'][0][1]
    temp_file.offset = val['background_params'][0][0]
    temp_file.error = val['error'][0][0]
    temp_file.r2 = val['r_squared'][0][0]
    peak = val['peak_params']
    for x in peak:
        temp_file.peak_freq.append(x[0])
        temp_file.freq_area.append(x[1]*x[2])
    return temp_file

def extract_fooof_main(data_path_path):
    before = time.time()
    data_path =  data_path_path
    print('Adding MatLab Path...')
    matlabEngine = matlab.engine.start_matlab()
    matlabEngine.loadPath(nargout = 0)
    print('This is your data path: ' +  data_path)
    file_dir = find_file_directory(data_path)

    all_files_data = []
    all_patient_numbers = []
    files_to_ignore = read_file_names('discard.txt')

    for file in file_dir:
        all_files_data.append(extract_single_file_data(file))
    for file in all_files_data:
        if patient_number.search(file.name)[1] not in all_patient_numbers:
            all_patient_numbers.append(patient_number.search(file.name)[1])

    wb = openpyxl.Workbook()
    for patient in all_patient_numbers:
        sheet = wb.create_sheet(patient)
        sheet['A1'] = 'File Name'
        sheet['B1'] = 'Slope'
        sheet['C1'] = 'Offset'
        sheet['D1'] = 'Error'
        sheet['E1'] = 'R2'
        sheet['F1'] = 'Peak'
        sheet['G1'] = 'Area'
        index = 2
        for file in all_files_data:
            if patient_number.search(file.name)[1] == patient:
                sheet['A' + str(index)] = file.name
                if file.name in files_to_ignore:
                    index += 1
                else:
                    sheet['A' + str(index)] = file.name
                    sheet['B' + str(index)] = file.exponent
                    sheet['C' + str(index)] = file.offset
                    sheet['D' + str(index)] = file.error
                    sheet['E' + str(index)] = file.r2
                    for index_peak, peaks in enumerate(file.peak_freq):
                        sheet['F' + str(index + index_peak)] = peaks
                        sheet['G' + str(index + index_peak)] = file.freq_area[index_peak]
                        index_peakk = index_peak
                    index = index + index_peakk + 1
    wb.save(data_path + '/Extracted Data.xlsx')
    print('Done Extracting Data into Excel File')
