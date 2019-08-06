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
        #print('Divide by 0') #Super annoying as it prints a lot
        return 0
def get_sum(list):
    try:
        return sum(list)
    except:
        #print('Nothing in List')
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
        sheet['F1'] = 'Delta Area'
        sheet['G1'] = 'Theta Area'
        sheet['H1'] = 'Alpha Area'
        sheet['I1'] = 'Beta Area'
        sheet['J1'] = 'Low Beta Area'
        sheet['K1'] = 'High Beta Area'
        sheet['L1'] = 'Gamma Area'
        sheet['M1'] = 'Peak'
        sheet['N1'] = 'Area'
        index = 2
        freq_index = 2
        for patient_mm_file in patient.mm_files:
            mm_exponents = []
            mm_offset = []
            mm_r2 = []
            mm_error =[]
            mm_peak = []
            mm_area = []
            mm_delta = []
            mm_theta = []
            mm_alpha = []
            mm_low_beta = []
            mm_high_beta = []
            mm_beta = []
            mm_gamma = []
            for segment in patient_mm_file.segments:
                mm_exponents.append(segment.exponent)
                mm_offset.append(segment.offset)
                mm_r2.append(segment.r2)
                mm_error.append(segment.error)
                for index_freq, freq in enumerate(segment.peak_freq):
                    mm_peak.append(freq)
                    mm_area.append(segment.freq_area[index_freq])

                    if freq <= 4:
                        mm_delta.append(freq)
                    elif freq > 4 and freq <= 8:
                        mm_theta.append(freq)
                    elif freq > 8 and freq <= 13:
                        mm_alpha.append(freq)
                    elif freq > 13 and freq <= 20:
                        mm_low_beta.append(freq)
                    elif freq > 20 and freq <= 35:
                        mm_high_beta.append(freq)
                    elif freq > 35 and freq <= 50:
                        mm_gamma.append(freq)
                    if freq > 13 and freq <= 35:
                        mm_beta.append(freq)

            mm_exponents = get_average(mm_exponents)
            mm_offset = get_average(mm_offset)
            mm_r2 = get_average(mm_r2)
            mm_error = get_average(mm_error)
            mm_delta = get_sum(mm_delta)
            mm_theta = get_sum(mm_theta)
            mm_alpha = get_sum(mm_alpha)
            mm_low_beta = get_sum(mm_low_beta)
            mm_high_beta = get_sum(mm_high_beta)
            mm_beta = get_sum(mm_beta)
            mm_gamma = get_sum(mm_gamma)

            sheet['A' + str(index)] = patient_mm_file.name
            sheet['B' + str(index)] = mm_exponents
            sheet['C' + str(index)] = mm_offset
            sheet['D' + str(index)] = mm_error
            sheet['E' + str(index)] = mm_r2
            sheet['F' + str(index)] = mm_delta
            sheet['G' + str(index)] = mm_theta
            sheet['H' + str(index)] = mm_alpha
            sheet['I' + str(index)] = mm_beta
            sheet['J' + str(index)] = mm_low_beta
            sheet['K' + str(index)] = mm_high_beta
            sheet['L' + str(index)] = mm_gamma

            index += 1
            for index_peak, peak in enumerate(mm_peak):
                sheet['M' + str(freq_index)] = peak
                sheet['N' + str(freq_index)] = mm_area[index_peak]
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

def add_brain_section_averages(brain_sections_array, work_book):
    sheet = work_book.create_sheet('Averages')
    sheet['A1'] = 'Name'
    sheet['B1'] = 'Slope'
    sheet['C1'] = 'Offset'
    sheet['D1'] = 'Error'
    sheet['E1'] = 'R2'
    for section_index, section in enumerate(brain_sections_array):
        sheet['A' + str(section_index + 2)] = section.name
        sheet['B' + str(section_index + 2)] = get_average(section.average_exponents)
        sheet['C' + str(section_index + 2)] = get_average(section.average_offset)
        sheet['D' + str(section_index + 2)] = get_average(section.average_error)
        sheet['E' + str(section_index + 2)] = get_average(section.average_r2)
    return

#In Progress the function is broken right now and does basically nothing
def add_averages_to_patient_data(brain_section_names_array, brain_section_values_array,work_book, patients):
    #Use this function after the inital workbook as been created as this appends on to it
    #Order of the arrays must be the same
    for patient in patients:
        sheet = work_book[str(patient.name)]
        ld = BrainSection('LD')
        lv = BrainSection('lv')
        rd = BrainSection('rd')
        rv = BrainSection('rv')
        names = []
        slopes = []
        offset = []
        r2 = []
        error = []
        delta = []
        theta = []
        alpha = []
        low_beta = []
        high_beta = []
        beta = []
        gamma = []
        for cell in sheet['A']:
            names.append(cell.value)
        for cell in sheet['B']:
            slopes.append(cell.value)
        for cell in sheet['C']:
            offset.append(cell.value)
        for cell in sheet['D']:
            error.append(cell.value)
        for cell in sheet['E']:
            r2.append(cell.value)
        for cell in sheet['F']:
            delta.append(cell.value)
        for cell in sheet['G']:
            theta.append(cell.value)
        for cell in sheet['H']:
            alpha.append(cell.value)
        for cell in sheet['I']:
            beta.append(cell.value)
        for cell in sheet['J']:
            low_beta.append(cell.value)
        for cell in sheet['K']:
            high_beta.append(cell.value)
        for cell in sheet['L']:
            gamma.append(cell.value)
        #Ignore index 0 as that just has the name of the column
        for section_index, section in enumerate(brain_section_names_array):
            bsection = BrainSection('Section')
            for file_name in section:
                for name_index, name in enumerate(names):
                    if name == file_name:
                        print(file_name)
                        bsection.average_exponents.append(slopes[name_index])
                        bsection.average_offset.append(offset[name_index])
                        bsection.average_r2.append(r2[name_index])
                        bsection.average_error.append(error[name_index])
                        bsection.delta_freq_area.append(delta[name_index])
                        bsection.theta_freq_area.append(theta[name_index])
                        bsection.alpha_freq_area.append(alpha[name_index])
                        bsection.beta_freq_area.append(beta[name_index])
                        bsection.low_beta_freq_area.append(low_beta[name_index])
                        bsection.high_beta_freq_area.append(high_beta[name_index])
                        bsection.gamma_freq_area.append(gamma[name_index])

            first_empty_index = names.index(None) + 2
            sheet['A' + str(first_empty_index + section_index)] = brain_section_values_array[section_index].name
            sheet['B' + str(first_empty_index + section_index)] = get_average(bsection.average_exponents)
            sheet['C' + str(first_empty_index + section_index)] = get_average(bsection.average_offset)
            sheet['D' + str(first_empty_index + section_index)] = get_average(bsection.average_error)
            sheet['E' + str(first_empty_index + section_index)] = get_average(bsection.average_r2)

            sheet['F' + str(first_empty_index + section_index)] = get_sum(bsection.delta_freq_area)
            sheet['G' + str(first_empty_index + section_index)] = get_sum(bsection.theta_freq_area)
            sheet['H' + str(first_empty_index + section_index)] = get_sum(bsection.alpha_freq_area)
            sheet['I' + str(first_empty_index + section_index)] = get_sum(bsection.beta_freq_area)
            sheet['J' + str(first_empty_index + section_index)] = get_sum(bsection.low_beta_freq_area)
            sheet['K' + str(first_empty_index + section_index)] = get_sum(bsection.high_beta_freq_area)
            sheet['L' + str(first_empty_index + section_index)] = get_sum(bsection.gamma_freq_area)
