import time
import os
import re
import matlab.engine

def create_fooof_main(data_path_path):
    before = time.time()
    eng = matlab.engine.start_matlab()

    print('Adding Paths....')
    eng.loadPath(nargout = 0) # Need this loadPath file in your MATLAB directory
    print('Ignore the Warnings.')
    print('Will create figures in the background, you can continue to do other work')
    print('\n' * 2)
    dataPath = data_path_path # This is where all your data should be store, this contains folders with patient numbers in which the smr files are contained

    names = [] #Finding the directory, locating all the smr files and saving their directories into a list
    for root, dirs, files in os.walk(dataPath):
        for file in files:
            if file.endswith('.smr'):
                names.append(os.path.join(root, file)) #stored the directory with the name.
    patients=[]
    oldNumber = 0;
    findPatientNumber = re.compile(r'/Data/(\d\d\d\d)/')
    for x in names:
        number = findPatientNumber.search(x)
        if number:
            number = int(number.group(1))
            if number != oldNumber: #Making sure to not add the same patient twice, and updating the matlab save file directory, you can add any patient you want to skip over here
                patients.append(number) #updating the patients we have
                #Going to update the matlab file to change the save location
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
    after = time.time()
    print('Time taken:' + str(after-before))
    print('Done creating Fooof Files!')
