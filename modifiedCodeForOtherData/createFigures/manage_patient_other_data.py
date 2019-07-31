import re
import openpyxl
import scipy.io as sio
from data_structure import Patient
from data_structure import BrainSection
from data_structure import SegmentFile
from data_structure import MM
from figure_creation import create_figure

find_patient_number_re = re.compile(r'(OtherData/)(\d\d\d\d)')
file_name_result = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')
file_name = re.compile(r'(\d\d\d\d)(-\d\d\d\d)([ABCDEF])?')

def get_average(list):
    try:
        return sum(list) / len(list)
    except:
        print('Divide by Zero')
        return 0
def get_sum(list):
    try:
        return sum(list)
    except:
        print('Nothing in List')
        return 0

def extract_single_file_data(file_name):
    file_content = sio.loadmat(file_name)
    struct = file_content['fooof_results']
    temp_file = SegmentFile(file_name_result.search(file_name)[0])
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

def find_patient_number(file_directory):
    patient_numbers = []
    patients = []
    for file in file_directory:
        if find_patient_number_re.search(file)[2] not in patient_numbers:
            patients.append(Patient(find_patient_number_re.search(file)[2]))
            patient_numbers.append(find_patient_number_re.search(file)[2])
    return patients

def find_segments_for_patient(file_directory, patients, r2_tolerance, do_not_run):
    for file in file_directory:
        for patient in patients:
            if patient.name == file_name.search(file)[1]: # if the files patient number matches that is xxxx- matches
                if file_name.search(file)[0] not in patient.mm_files_names:
                    patient.mm_files_names.append(file_name.search(file)[0])
                    patient.mm_files.append(MM(file_name.search(file)[0])) # Creating the mm file, with its name xxxx-xxxxC, if it doesnt exist
                mm_file_index = patient.mm_files_names.index(file_name.search(file)[0]) # getting the index of xxxx-xxxxC
                data = extract_single_file_data(file)
                if file_name_result.search(file)[0] in do_not_run or data.r2 < r2_tolerance:
                    continue
                else:
                    patient.mm_files[mm_file_index].segments.append(data)

def fill_raw_excel(work_book, patients):
    for patient in patients:
        sheet_name = str(patient.name)
        sheet = work_book.create_sheet(sheet_name)
        sheet['A1'] = 'MM Name'
        sheet['B1'] = 'Slope'
        sheet['C1'] = 'Offset'
        sheet['D1'] = 'Error'
        sheet['E1'] = 'R2'
        sheet['F1'] = 'Peak'
        sheet['G1'] = 'Area'
        index = 2
        freq_index = 2
        for patient_mm_file in patient.mm_files:
            mm_exponents = []
            mm_offset = []
            mm_r2 = []
            mm_error =[]
            mm_peak = []
            mm_area = []
            for segment in patient_mm_file.segments:
                mm_exponents.append(segment.exponent)
                mm_offset.append(segment.offset)
                mm_r2.append(segment.r2)
                mm_error.append(segment.error)
                for index_freq, freq in enumerate(segment.peak_freq):
                    mm_peak.append(freq)
                    mm_area.append(segment.freq_area[index_freq])
            mm_exponents = get_average(mm_exponents)
            mm_offset = get_average(mm_offset)
            mm_r2 = get_average(mm_r2)
            mm_error = get_average(mm_error)
            sheet['A' + str(index)] = patient_mm_file.name
            sheet['B' + str(index)] = mm_exponents
            sheet['C' + str(index)] = mm_offset
            sheet['D' + str(index)] = mm_error
            sheet['E' + str(index)] = mm_r2
            index += 1
            for index_peak, peak in enumerate(mm_peak):
                sheet['F' + str(freq_index)] = peak
                sheet['G' + str(freq_index)] = mm_area[index_peak]
                freq_index += 1

def fill_brain_section(name, patients, brain_area):
    brain_section =  BrainSection(name)
    for brain_area_mm_file in brain_area:
        for patient in patients:
            for patient_mm_file in patient.mm_files:
                if brain_area_mm_file == patient_mm_file.name:
                    mm_exponents = []
                    mm_offset = []
                    mm_r2 = []
                    mm_error =[]
                    mm_peak = []
                    mm_area = []
                    for segment in patient_mm_file.segments:
                        mm_exponents.append(segment.exponent)
                        mm_offset.append(segment.offset)
                        mm_r2.append(segment.r2)
                        mm_error.append(segment.error)
                        for index_freq, freq in enumerate(segment.peak_freq):
                            mm_peak.append(freq)
                            mm_area.append(segment.freq_area[index_freq])
                    brain_section.average_exponents.append(get_average(mm_exponents))
                    brain_section.average_offset.append(get_average(mm_offset))
                    brain_section.average_r2.append(get_average(mm_r2))
                    brain_section.average_error.append(get_average(mm_error))
                    for index_peak, peak in enumerate(mm_peak):
                        brain_section.peak_freq.append(peak)
                        brain_section.freq_area.append(mm_area[index_peak])
    return brain_section

def remove_empty_data_from_brain_section(brain_section):
    number_of_empty_data = brain_section.average_exponents.count(0)
    print(number_of_empty_data)
    if number_of_empty_data == 0:
        return
    i = 0
    while i < number_of_empty_data:
        index_of_data = brain_section.average_exponents.index(0)
        brain_section.average_exponents.pop(index_of_data)
        brain_section.average_offset.pop(index_of_data)
        brain_section.average_r2.pop(index_of_data)
        brain_section.average_error.pop(index_of_data)
        i += 1
