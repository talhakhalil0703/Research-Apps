import os
import re
import matlab.engine
eng = matlab.engine.start_matlab()

print('Adding Paths....')
eng.loadPath(nargout = 0)
print(' Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/Research/Data' # This is where all your data should be store, this contains folders with patient numbers in which the smr files are contained

names = [] #Finding the directory, locating all the smr files and saving their directories into a list
for root, dirs, files in os.walk(dataPath):
    for file in files:
        if file.endswith('.smr'):
            names.append(os.path.join(root, file)) #stored the directory with the name.

patients = []
oldNumber = 0;
findPatientNumber = re.compile(r'/Data/(\d\d\d\d)/')
for x in names:
    number = findPatientNumber.search(x)
    if number:
        number = int(number.group(1))
        if number == 2130 and number != oldNumber: #Making sure to not add the same patient twice, and updating the matlab save file directory, you can add any patient you want to skip over here
            patients.append(number) #updating the patients we have
            #Going to update the matlab file to change the save location
            file = open('/Users/talhakhalil/Documents/MATLAB/smr_conversion_auto_FOOOF.m', 'r') #Reading the file
            fileContent = file.read() #Saving the files content into a string
            filePatientNumber = findPatientNumber.search(fileContent) #searching for the patient number, just incase
            filePatientNumber = int(filePatientNumber.group(1)) #converting the string number to type int
            file.close() #Closing the file to reopen so we can write to it now
           
            newContent= fileContent.replace("/Data/%d" %(filePatientNumber), "/Data/%d" %(number), 5) #replacing the old patient number with the new one, and saving it to a string

            file = open('/Users/talhakhalil/Documents/MATLAB/smr_conversion_auto_FOOOF.m', 'w') #Writing to the file
            file.write(newContent)
            file.close() # Closing the file as to not mess it up by accident.

            searchPath = dataPath + '/%d' %(number) + '/' #This now points to the patients folder which contains the smr files
            fileName = re.compile(r'%s(\d\d\d\d-\d\d\d\d)([ABCDEFabcdef])?' %(searchPath));
            for y in names:
                figureCreate = fileName.search(y) #Finds the first smr file to work with
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
                    eng.smr_conversion_auto_FOOOF(searchName, 10, 1000, searchPath , searchPath , nargout = 0)
            print('Finished creating figures for patient, ' + str(number))
            oldNumber = number #Making sure to not add the same patient twice
