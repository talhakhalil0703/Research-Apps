import openpyxl
from data_structure import BrainSection
from manage_patient_data import extract_mm_from_middle
from manage_patient_data import get_average
from figure_creation import create_figure
from figure_creation import create_slope_mm

def add_averages_to_excel_file(patient_array, max_mm, do_not_run_mm, work_book, data_path, bin_peak, bin_area, palpha):
    slopes_per_mm = [None] * max_mm * 2
    sheet = work_book.create_sheet('Patients Average Data')
    x = 1
    while x <= max_mm:
        dorsal = BrainSection('Dorsal')
        ventral = BrainSection('Ventral')
        extract_mm_from_middle(patient_array, dorsal, ventral, x, do_not_run_mm)
        slopes_per_mm[max_mm - x] = dorsal.exponents.copy()
        slopes_per_mm[max_mm + x - 1] = ventral.exponents.copy()
        sheet['A' + str(x)] = 'Points in: ' + str(x) + ' mm: ' + str(len(dorsal.average_error))
        sheet['B' + str(x)] = 'Dorsal Slope Average For : ' + str(x) + ' mm'
        sheet['C' + str(x)] = get_average(dorsal.average_exponents)
        sheet['D' + str(x)] = 'Dorsal Offset Average For : ' + str(x) + ' mm'
        sheet['E' + str(x)] = get_average(dorsal.average_offset)
        sheet['F' + str(x)] =  'Points in: ' + str(x) + ' mm: ' + str(len(ventral.average_error))
        sheet['G' + str(x)] = 'Ventral Slope Average For : ' + str(x) + ' mm'
        sheet['H' + str(x)] = get_average(ventral.average_exponents)
        sheet['I' + str(x)] = 'Ventral Offset Average For : ' + str(x) + ' mm'
        sheet['J' + str(x)] = get_average(ventral.average_offset)
        create_figure('Dorsal ' + str(x) + 'mm', data_path, dorsal, bin_peak, bin_area, palpha)
        create_figure('Ventral ' + str(x) + 'mm', data_path, ventral, bin_peak, bin_area, palpha)
        x += 1
    create_slope_mm('Slopes VS MM', data_path, slopes_per_mm)
class Do_NOT(Exception):
    pass

def store_all_patients_raw_data(patient_array, work_book, do_not_run_mm):
    for patient in patient_array:
        for index, trajectory in enumerate(patient.trajectory_number):
            sheet_name = str(patient.name) + '_' + str(index)
            sheet = work_book.create_sheet(sheet_name)
            sheet['A1'] = 'Slope'
            sheet['B1'] = 'Offset'
            sheet['C1'] = 'Error'
            sheet['D1'] = 'R2'
            sheet['E1'] = 'Peak'
            sheet['F1'] = 'Area'
            mm_freq, mm_area = [], []
            for mm_index, MM in enumerate(trajectory):
                try:
                    mm_exp, mm_offset, mm_r2, mm_error = [], [], [], []
                    for do_not_include in do_not_run_mm:
                        if do_not_include == MM.name:
                            raise Do_NOT()
                    for segment in MM.mm_files:
                        mm_exp.append(segment.exponent)
                        mm_offset.append(segment.offset)
                        mm_r2.append(segment.r2)
                        mm_error.append(segment.error)
                        for index_freq, freq in enumerate(segment.peak_freq):
                            mm_freq.append(segment.peak_freq[index_freq])
                            mm_area.append(segment.freq_area[index_freq])
                    sheet['A' + str(mm_index + 2)] = get_average(mm_exp)
                    sheet['B' + str(mm_index + 2)] = get_average(mm_offset)
                    sheet['C' + str(mm_index + 2)] = get_average(mm_r2)
                    sheet['D' + str(mm_index + 2)] = get_average(mm_error)
                except Do_NOT:
                    continue
                    
            for index_freq, freq in enumerate(mm_freq):
                sheet['E' + str(index_freq + 2)] = freq
                sheet['F' + str(index_freq + 2)] = mm_area[index_freq]
