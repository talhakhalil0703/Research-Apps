import time
import numpy
import openpyxl
import matlab.engine

from data_structure import BrainSection
from file_handle import find_file_directory
from file_handle import find_files
from file_handle import remove_files
from file_handle import read_file_names
from manage_patient_other_data import fill_raw_excel
from manage_patient_other_data import fill_brain_section
from manage_patient_other_data import find_patient_number
from manage_patient_other_data import find_segments_for_patient
from manage_patient_other_data import remove_empty_data_from_brain_section
from manage_patient_other_data import add_brain_section_averages
from figure_creation import create_figure

def main(string_data_path, string_r2, peak_array, area_array, string_alpha):

    before = time.time()

    data_path =  string_data_path
    r2_tolerance = float(string_r2)
    p1, p2, p3  = peak_array[0], peak_array[1], peak_array[2]
    bin_peak = list(numpy.arange(p1,p2,p3))
    p1, p2, p3 = area_array[0], area_array[1], area_array[2]
    bin_area = list(numpy.arange(p1,p2,p3))
    point_alpha = float(string_alpha)
    print('Adding MatLab Path...')
    matlabEngine = matlab.engine.start_matlab()
    matlabEngine.loadPath(nargout = 0)
    print('This is your data path: ' +  data_path)

    do_not_run_segment = read_file_names(data_path + '/TossData.txt')
    do_not_run_mm = read_file_names(data_path + '/mmToNotRun.txt')
    left_dorsal = read_file_names(data_path + '/dorsalLeft.txt')
    right_dorsal = read_file_names(data_path + '/dorsalRight.txt')
    left_ventral = read_file_names(data_path + '/ventralLeft.txt')
    right_ventral = read_file_names(data_path + '/ventralRight.txt')

    file_directory = find_file_directory(data_path)
    patients = find_patient_number(file_directory)
    find_segments_for_patient(file_directory, patients, r2_tolerance, do_not_run_segment)

    brain_section_left_dorsal = fill_brain_section('Left Dorsal', patients, left_dorsal)
    brain_section_right_dorsal = fill_brain_section('Right Dorsal', patients, right_dorsal)
    brain_section_left_ventral = fill_brain_section('Left Ventral', patients, left_ventral)
    brain_section_right_ventral = fill_brain_section('Right Ventral', patients, right_ventral)

    remove_empty_data_from_brain_section(brain_section_left_dorsal)
    remove_empty_data_from_brain_section(brain_section_right_dorsal)
    remove_empty_data_from_brain_section(brain_section_left_ventral)
    remove_empty_data_from_brain_section(brain_section_right_ventral)

    create_figure('Left Dorsal', data_path, brain_section_left_dorsal, bin_peak, bin_area, point_alpha)
    create_figure('Right Dorsal', data_path, brain_section_right_dorsal, bin_peak, bin_area, point_alpha)
    create_figure('Left Ventral', data_path, brain_section_left_ventral, bin_peak, bin_area, point_alpha)
    create_figure('Right Ventral', data_path, brain_section_right_ventral, bin_peak, bin_area, point_alpha)

    work_book = openpyxl.Workbook()
    fill_raw_excel(work_book, patients)
    add_brain_section_averages([brain_section_left_dorsal,brain_section_right_dorsal,brain_section_left_ventral, brain_section_right_ventral ], work_book)
    work_book.save(data_path + '/Patients Data.xlsx')

    after = time.time()
    print('Time Taken: ' + str(after-before))
