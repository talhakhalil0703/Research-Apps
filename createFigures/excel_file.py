import openpyxl
from data_structure import BrainSection
from manage_patient_data import extract_mm_from_middle
from manage_patient_data import get_average
from manage_patient_data import get_sum
from figure_creation import create_figure
from figure_creation import create_slope_mm

def append_data(original, data_to_append, data_to_append_2):
    len_of_original = len(original)
    temp = [None] * (len_of_original + 2)
    for index, x in enumerate(original):
        temp[index + 1] = x.copy()
    temp[0] = data_to_append
    temp[-1] = data_to_append_2

    return temp

def add_averages_to_excel_file(patient_array, max_mm, do_not_run_mm, work_book, data_path, bin_peak, bin_area, palpha):

    slopes_per_mm = [None] * max_mm * 2
    beta_freq_area_per_mm = [None] * max_mm * 2
    delta_freq_area_per_mm = [None] * max_mm * 2
    theta_freq_area_per_mm = [None] * max_mm * 2
    alpha_freq_area_per_mm = [None] * max_mm * 2
    low_beta_freq_area_per_mm = [None] * max_mm * 2
    high_beta_freq_area_per_mm = [None] * max_mm * 2
    gamma_freq_area_per_mm = [None] * max_mm * 2

    sheet = work_book.create_sheet('Patients Average Data')
    x = 1
    while x <= max_mm:
        dorsal = BrainSection('Dorsal')
        ventral = BrainSection('Ventral')
        dorsal_extreme = BrainSection('Dorsal Extreme')
        ventral_extreme = BrainSection('Ventral Extreme')
        extract_mm_from_middle(patient_array, dorsal, ventral, x, do_not_run_mm, dorsal_extreme, ventral_extreme)

        slopes_per_mm[max_mm - x] = dorsal.exponents.copy()
        slopes_per_mm[max_mm + x - 1] = ventral.exponents.copy()
        beta_freq_area_per_mm[max_mm - x] = dorsal.beta_freq_area.copy()
        beta_freq_area_per_mm[max_mm - 1 + x] = ventral.beta_freq_area.copy()
        delta_freq_area_per_mm[max_mm - x] = dorsal.delta_freq_area.copy()
        delta_freq_area_per_mm[max_mm - 1 + x] = ventral.delta_freq_area.copy()
        theta_freq_area_per_mm[max_mm - x] = dorsal.theta_freq_area.copy()
        theta_freq_area_per_mm[max_mm - 1 + x] = ventral.theta_freq_area.copy()
        alpha_freq_area_per_mm[max_mm - x] = dorsal.alpha_freq_area.copy()
        alpha_freq_area_per_mm[max_mm - 1 + x] = ventral.alpha_freq_area.copy()
        low_beta_freq_area_per_mm[max_mm - x] = dorsal.low_beta_freq_area.copy()
        low_beta_freq_area_per_mm[max_mm - 1 + x] = ventral.low_beta_freq_area.copy()
        high_beta_freq_area_per_mm[max_mm - x] = dorsal.high_beta_freq_area.copy()
        high_beta_freq_area_per_mm[max_mm - 1 + x] = ventral.high_beta_freq_area.copy()
        gamma_freq_area_per_mm[max_mm - x] = dorsal.gamma_freq_area.copy()
        gamma_freq_area_per_mm[max_mm - 1 + x] = ventral.gamma_freq_area.copy()

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

    slopes_per_mm = append_data(slopes_per_mm, dorsal_extreme.exponents, ventral_extreme.exponents)
    beta_freq_area_per_mm = append_data(beta_freq_area_per_mm, dorsal_extreme.beta_freq_area, ventral_extreme.beta_freq_area)
    delta_freq_area_per_mm = append_data(delta_freq_area_per_mm, dorsal_extreme.delta_freq_area, ventral_extreme.delta_freq_area)
    theta_freq_area_per_mm = append_data(theta_freq_area_per_mm, dorsal_extreme.theta_freq_area, ventral_extreme.theta_freq_area)
    alpha_freq_area_per_mm = append_data(alpha_freq_area_per_mm, dorsal_extreme.alpha_freq_area, ventral_extreme.alpha_freq_area)
    low_beta_freq_area_per_mm = append_data(low_beta_freq_area_per_mm, dorsal_extreme.low_beta_freq_area, ventral_extreme.low_beta_freq_area)
    high_beta_freq_area_per_mm = append_data(high_beta_freq_area_per_mm, dorsal_extreme.high_beta_freq_area, ventral_extreme.high_beta_freq_area)
    gamma_freq_area_per_mm = append_data(gamma_freq_area_per_mm, dorsal_extreme.gamma_freq_area, ventral_extreme.gamma_freq_area)

    create_slope_mm('Slopes', data_path, slopes_per_mm)
    create_slope_mm('Beta Freq Area', data_path, beta_freq_area_per_mm)
    create_slope_mm('Delta Freq Area', data_path, delta_freq_area_per_mm)
    create_slope_mm('Theta Freq Area', data_path, theta_freq_area_per_mm)
    create_slope_mm('Alpha Freq Area', data_path, alpha_freq_area_per_mm)
    create_slope_mm('Low Beta Freq Area', data_path, low_beta_freq_area_per_mm)
    create_slope_mm('High Beta Freq Area', data_path, high_beta_freq_area_per_mm)
    create_slope_mm('Gamma Freq Area', data_path, gamma_freq_area_per_mm)

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
            sheet['G1'] = 'Delta Area'
            sheet['H1'] = 'Theta Area'
            sheet['I1'] = 'Alpha Area'
            sheet['J1'] = 'Low Beta Area'
            sheet['K1'] = 'High Beta Area'
            sheet['L1'] = 'Gamma Area'
            mm_freq, mm_area = [], []
            for mm_index, MM in enumerate(trajectory):
                try:
                    mm_exp, mm_offset, mm_r2, mm_error = [], [], [], []
                    mm_delta_area, mm_theta_area, mm_alpha_area, mm_low_beta_area, mm_high_beta_area, mm_gamma_area = [], [], [], [], [], []

                    for do_not_include in do_not_run_mm:
                        if do_not_include == MM.name:
                            raise Do_NOT()
                    for segment in MM.mm_files:
                        mm_exp.append(segment.exponent)
                        mm_offset.append(segment.offset)
                        mm_r2.append(segment.r2)
                        mm_error.append(segment.error)
                        segment_delta_area, segment_theta_area, segment_alpha_area, segment_low_beta_area, segment_high_beta_area, segment_gamma_area = [], [], [], [], [], []
                        for index_freq, freq in enumerate(segment.peak_freq):
                            mm_freq.append(segment.peak_freq[index_freq])
                            mm_area.append(segment.freq_area[index_freq])

                            if segment.peak_freq[index_freq] <= 4:
                                segment_delta_area.append(segment.freq_area[index_freq])
                            elif segment.peak_freq[index_freq] > 4 and segment.peak_freq[index_freq] <= 8:
                                segment_theta_area.append(segment.freq_area[index_freq])
                            elif segment.peak_freq[index_freq] > 8 and segment.peak_freq[index_freq] <= 13:
                                segment_alpha_area.append(segment.freq_area[index_freq])
                            elif segment.peak_freq[index_freq] > 13 and segment.peak_freq[index_freq] <= 20:
                                segment_low_beta_area.append(segment.freq_area[index_freq])
                            elif segment.peak_freq[index_freq] > 20 and segment.peak_freq[index_freq] <= 35:
                                segment_high_beta_area.append(segment.freq_area[index_freq])
                            elif segment.peak_freq[index_freq] > 35 and segment.peak_freq[index_freq] <= 50:
                                segment_gamma_area.append(segment.freq_area[index_freq])
                        mm_delta_area.append(get_sum(segment_delta_area))
                        mm_theta_area.append(get_sum(segment_theta_area))
                        mm_alpha_area.append(get_sum(segment_alpha_area))
                        mm_low_beta_area.append(get_sum(segment_low_beta_area))
                        mm_high_beta_area.append(get_sum(segment_high_beta_area))
                        mm_gamma_area.append(get_sum(segment_gamma_area))

                    sheet['A' + str(mm_index + 2)] = get_average(mm_exp)
                    sheet['B' + str(mm_index + 2)] = get_average(mm_offset)
                    sheet['C' + str(mm_index + 2)] = get_average(mm_r2)
                    sheet['D' + str(mm_index + 2)] = get_average(mm_error)
                    sheet['G' + str(mm_index + 2)] = get_sum(mm_delta_area)
                    sheet['H' + str(mm_index + 2)] = get_sum(mm_theta_area)
                    sheet['I' + str(mm_index + 2)] = get_sum(mm_alpha_area)
                    sheet['J' + str(mm_index + 2)] = get_sum(mm_low_beta_area)
                    sheet['K' + str(mm_index + 2)] = get_sum(mm_high_beta_area)
                    sheet['L' + str(mm_index + 2)] = get_sum(mm_gamma_area)
                except Do_NOT:
                    continue

            for index_freq, freq in enumerate(mm_freq):
                sheet['E' + str(index_freq + 2)] = freq
                sheet['F' + str(index_freq + 2)] = mm_area[index_freq]
