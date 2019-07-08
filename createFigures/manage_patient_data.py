import re
import scipy.io as sio
from data_structure import Patient
from data_structure import MM
from data_structure import BrainSection
from data_structure import SegmentFile

find_patient_number = re.compile(r'(\d\d\d\d)(-)')
file_name = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?')

def get_average(list):
    try:
        return sum(list) / len(list)
    except:
        print('Divide by Zero')
        return 0


def find_start_end_trajectories(data_path, trajectories):
    start_trajectories = []
    end_trajectories = []
    end_of_trajectory = False
    for x in trajectories:
        if end_of_trajectory is True:
            end_trajectories.append(x)
            end_of_trajectory = False
        else:
           start_trajectories.append(x)
           end_of_trajectory = True
    return start_trajectories, end_trajectories

def fill_trajectories_for_patient(single_patient, start_trajectories,end_trajectories, all_files):
    for index, start_trajectory in enumerate(start_trajectories):
        if str(single_patient.name) == find_patient_number.search(start_trajectory)[1]:
            trajectory = []
            start_index = all_files.index(start_trajectory)
            end_index = all_files.index(end_trajectories[index])
            i = start_index
            while i <= end_index:
                mm_file = MM(all_files[i])
                trajectory.append(mm_file)
                i += 1
            print(len(trajectory))
            single_patient.trajectory_number.append(trajectory)

def create_patient_array_with_trajectories(data_path, trajectories, all_files):
    start_trajectories, end_trajectories = find_start_end_trajectories(data_path, trajectories)
    patient_array = []
    old_patient = 0
    patient_number = None
    for start_trajectory in start_trajectories:
        patient_number = find_patient_number.search(start_trajectory)
        patient_number = int(patient_number.group(1))
        if patient_number != old_patient:
            y = Patient(patient_number)
            fill_trajectories_for_patient(y, start_trajectories, end_trajectories, all_files)
            patient_array.append(y)
            old_patient = patient_number
    return patient_array

def extract_single_file_data(single_patient, file_name, data_path):
    file_content = sio.loadmat(data_path + '/' + str(single_patient.name) + '/' + file_name + '_fooof_results.mat')
    struct = file_content['fooof_results']
    temp_file = SegmentFile(file_name)
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

def extract_data_for_patient(single_patient, all_result_files, data_path, r2_tolerance):
    for trajectory in single_patient.trajectory_number:
        for mm_file in trajectory:
            for single_file in all_result_files:
                if mm_file.name == file_name.search(single_file)[0]:
                    temp_file = extract_single_file_data(single_patient, single_file, data_path)
                    if temp_file.r2 >= r2_tolerance:
                        mm_file.mm_files.append(temp_file)

def append_brain_section_for_mm(mm_file, brain_section):
    temp_exponent, temp_offset, temp_r2, temp_error = [], [], [], []
    for segment in mm_file.mm_files:
        temp_exponent.append(segment.exponent)
        temp_offset.append(segment.offset)
        temp_r2.append(segment.r2)
        temp_error.append(segment.error)

        brain_section.exponents.append(segment.exponent)
        brain_section.offset.append(segment.offset)
        brain_section.r2.append(segment.r2)
        brain_section.error.append(segment.error)

        for index, freq in enumerate(segment.peak_freq):
            brain_section.peak_freq.append(freq)
            brain_section.freq_area.append(segment.freq_area[index])

    brain_section.average_exponents.append(get_average(temp_exponent))
    brain_section.average_offset.append(get_average(temp_offset))
    brain_section.average_r2.append(get_average(temp_r2))
    brain_section.average_error.append(get_average(temp_error))

def extract_mm_from_middle(patient_array, dorsal, ventral, mm_to_extract, do_not_run_mm):
    for patient in patient_array:
        for trajectory in patient.trajectory_number:
            if len(trajectory) % 2 == 1:
                trajectory_length = len(trajectory) - 1
            else:
                trajectory_length = len(trajectory)
            ventral_index = trajectory_length // 2
            if mm_to_extract > ventral_index:
                return

            include_dorsal = True
            include_ventral = True
            for do_not_include in do_not_run_mm:
                if do_not_include == trajectory[ventral_index - mm_to_extract].name:
                    print('Excluding mm point'+ do_not_include)
                    include_dorsal = False
                if do_not_include == trajectory[ventral_index - 1 + mm_to_extract].name:
                    print('Excluding mm point'+ do_not_include)
                    include_ventral = False

            if include_dorsal:
                append_brain_section_for_mm(trajectory[ventral_index - mm_to_extract], dorsal)
            if include_ventral:
                append_brain_section_for_mm(trajectory[ventral_index - 1 + mm_to_extract], ventral)
