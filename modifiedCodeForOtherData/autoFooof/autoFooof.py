import time
import os
import re
import matlab.engine
before = time.time()
eng = matlab.engine.start_matlab()

print('Adding Paths....')
eng.loadPath(nargout = 0)
print(' Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/OtherData' # This is where all your data should be store, this contains folders with patient numbers in which the smr files are contained

names = [] #Finding the directory, locating all the smr files and saving their directories into a list
for root, dirs, files in os.walk(dataPath):
    for file in files:
        if file.endswith('.smr'):
            names.append(os.path.join(root, file)) #stored the directory with the name.

patients=[]
oldNumber = 0;
findPatientNumber = re.compile(r'/OtherData/(\d\d\d\d)/')
findPatientNumberLFP = re.compile(r'/OtherData/(\d\d\d\d)/LFP_1000_Hz/')
for x in names:
    number = findPatientNumber.search(x)
    if number:
        number = int(number.group(1))
        if number != oldNumber: #Making sure to not add the same patient twice, and updating the matlab save file directory, you can add any patient you want to skip over here
            patients.append(number) #updating the patients we have
            #Going to update the matlab file to change the save location
            searchPath = dataPath + '/%d' %(number) + '/' #This now points to the patients folder which contains the smr files
            searchPathLFP = dataPath + '/%d' %(number) + '/LFP_1000_Hz/' #This now points to the patients folder which contains the smr files
            fileName = re.compile(r'%s(\d\d\d\d-\d\d\d\d)([ABCDEFabcdef])?' %(searchPath));
            fileNameLFP = re.compile(r'%s(\d\d\d\d-\d\d\d\d)([ABCDEFabcdef])?' %(searchPathLFP));
            patient_time = time.time()
            for y in names:
                LFP = False
                figureCreate = fileName.search(y) #Finds the first smr file to work with
                if figureCreate == None:
                    figureCreate = fileNameLFP.search(y)
                    LFP = True
                    if figureCreate == None:
                        continue
                figureName = figureCreate.group(1,2)
                if figureName[0] != None: #Only runs code if the figure is found, or else we get an error
                    if figureName[1] != None:
                        searchName = figureName[0] + figureName[1]
                    else:
                        searchName = figureName[0]
                    searchName = str(searchName)
                    print(searchName) #Patient file name
                    if LFP == False:
                        eng.smr_conversion_auto_FOOOF(searchName, 10, 1000.0, searchPath , searchPath , nargout = 0)
                    else:
                        eng.smr_conversion_auto_FOOOF(searchName, 10, 1000.0, searchPathLFP , searchPathLFP , nargout = 0)
                        print('In LFP_1000_Hz')
            patient_time_end = time.time()
            print('Finished creating figures for patient, ' + str(number) + ' time taken : ' + str(patient_time_end - patient_time))
            print('Time elapsed: ' + str(patient_time_end-before))
            oldNumber = number #Making sure to not add the same patient twice
after = time.time()
print('Time taken:' + str(after-before))
