import time
import numpy
import openpyxl
import matlab.engine

from data_structure import BrainSection
from file_handle import find_file_directory
from file_handle import find_files
from file_handle import remove_files
from file_handle import read_file_names
from manage_patient_data import create_patient_array_with_trajectories
from manage_patient_data import extract_data_for_patient
from excel_file import add_averages_to_excel_file
from excel_file import store_all_patients_raw_data
def main (string_data_path, string_r2, peark_array, area_array, string_alpha, string_mm_to_choose):

    before = time.time()

    data_path =  string_data_path
    r2_tolerance = float(string_r2)
    p1, p2, p3  = peark_array[0], peark_array[1], peark_array[2]
    bin_peak = list(numpy.arange(p1,p2,p3))
    p1, p2, p3 = area_array[0], area_array[1], area_array[2]
    bin_area = list(numpy.arange(p1,p2,p3))
    max_mm = int(string_mm_to_choose)
    point_alpha = float(string_alpha)
    print('Adding MatLab Path...')
    matlabEngine = matlab.engine.start_matlab()
    matlabEngine.loadPath(nargout = 0)
    print('This is your data path: ' +  data_path)
    print('Going to test ' + string_mm_to_choose + ' away from the middle!')

    do_not_run_segment = read_file_names(data_path + '/TossData.txt')
    do_not_run_mm = read_file_names(data_path + '/mmToNotRun.txt')
    trajectories = read_file_names(data_path + '/Trajectories.txt')

    file_directory = find_file_directory(data_path)
    all_files = find_files(data_path, file_directory, False)
    all_result_files = find_files(data_path, file_directory, True)
    all_result_files = remove_files(all_result_files, do_not_run_segment)

    patient_array = create_patient_array_with_trajectories(data_path, trajectories,all_files)

    wb = openpyxl.Workbook()
    for patient in patient_array:
        extract_data_for_patient(patient, all_result_files, data_path, r2_tolerance)

    add_averages_to_excel_file(patient_array, max_mm, do_not_run_mm, wb, data_path, bin_peak, bin_area, point_alpha)
    store_all_patients_raw_data(patient_array, wb, do_not_run_mm)

    wb.save(data_path + '/Patients Data V2.xlsx')
    after = time.time()
    print('Time Taken: ' + str(after-before))
