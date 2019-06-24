def extractData(patientArray, dorsal, ventral, mm): #Goes from Dorsal and Ventral, and goes mmToTest millimeter away to collect data
    mmToTest = mm

    for x in patientArray:
        y = 0
        while y < x.getTractLen():
            dorsalIndex = x.getAllTrajectory(y).getTractLen() // 2
            z = 0
            while z < dorsalIndex:
                if z == 0: #ignoring the first mm
                    z += 1
                    continue
                if mmToTest != 0:
                    if z > (mmToTest):
                        z += 1
                        continue
                fileIndex = x.getAllTrajectory(y).getTract()[z].getResultsFilesLen()
                dorsal.appendAverageExponents(x.getAllTrajectory(y).getTract()[z].getAverageExponent())
                dorsal.appendAverageOffset(x.getAllTrajectory(y).getTract()[z].getAverageOffset())
                dorsal.appendAverageR2(x.getAllTrajectory(y).getTract()[z].getAverageR2())
                dorsal.appendAverageError(x.getAllTrajectory(y).getTract()[z].getAverageError())
                q = 0
                while q < fileIndex:
                    dorsal.appendExponents(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getExponent())
                    dorsal.appendOffset(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getOffset())
                    dorsal.appendError(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getError())
                    dorsal.appendR2(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getR2())
                    freqIndex = x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqLen()
                    o = 0
                    while o < freqIndex:
                        dorsal.appendPeakFreq(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreq()[o])
                        dorsal.appendFreqArea(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqArea()[o])
                        o += 1
                    q += 1
                z += 1

            while z < x.getAllTrajectory(y).getTractLen():
                if z == (x.getAllTrajectory(y).getTractLen() - 1): #ignoring the last mm
                    z += 1
                    continue
                if mmToTest != 0:
                    if z < (x.getAllTrajectory(y).getTractLen() - (mmToTest + 1)):
                        z += 1
                        continue
                fileIndex = x.getAllTrajectory(y).getTract()[z].getResultsFilesLen()
                ventral.appendAverageExponents(x.getAllTrajectory(y).getTract()[z].getAverageExponent())
                ventral.appendAverageOffset(x.getAllTrajectory(y).getTract()[z].getAverageOffset())
                ventral.appendAverageR2(x.getAllTrajectory(y).getTract()[z].getAverageR2())
                ventral.appendAverageError(x.getAllTrajectory(y).getTract()[z].getAverageError())
                q = 0
                while q < fileIndex:
                    ventral.appendExponents(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getExponent())
                    ventral.appendOffset(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getOffset())
                    ventral.appendError(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getError())
                    ventral.appendR2(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getR2())
                    freqIndex = x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqLen()
                    o = 0
                    while o < freqIndex:
                        ventral.appendPeakFreq(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreq()[o])
                        ventral.appendFreqArea(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqArea()[o])
                        o += 1
                    q += 1
                z += 1
            y += 1

    print('\n'*2 + 'Ignored the first and last mm!')
    print('Done seperating into Ventral and Dorsal groups!')

def extractDataFromMiddle(patientArray, dorsal, ventral, mmToTest):
    for x in patientArray:
        y = 0
        while y < x.getTractLen():

            tractLength = x.getAllTrajectory(y).getTractLen()
            if tractLength % 2 == 1:
                x.getAllTrajectory(y).removeTract(tractLength - 1)
                tractLength = x.getAllTrajectory(y).getTractLen()
                print('Cutout a mm from ventral to make length even for: ' +  str(x.getName()) + 'Tract ' + str(y))

            ventralIndex = tractLength // 2 #Ventral mm part starts at this index, below this index is dorsal

            if (mmToTest == 0):
                print('Cannot be 0 mm away from the middle')
                y += 1
                continue
            if (mmToTest > tractLength // 2):
                #print('No mm exists at this point for: ' + str(x.getName()) +' Tract ' + str(y) + ' '+ str(mmToTest))
                y += 1
                continue

            dorsal.appendAverageExponents(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getAverageExponent())
            dorsal.appendAverageOffset(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getAverageOffset())
            dorsal.appendAverageR2(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getAverageR2())
            dorsal.appendAverageError(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getAverageError())
            ventral.appendAverageExponents(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getAverageExponent())
            ventral.appendAverageOffset(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getAverageOffset())
            ventral.appendAverageR2(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getAverageR2())
            ventral.appendAverageError(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getAverageError())

            fileIndex = x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFilesLen()
            q = 0
            while q < fileIndex:
                dorsal.appendExponents(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getExponent())
                dorsal.appendOffset(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getOffset())
                dorsal.appendError(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getError())
                dorsal.appendR2(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getR2())
                freqIndex = x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getFreqLen()
                o = 0
                while o < freqIndex:
                    dorsal.appendPeakFreq(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getFreq()[o])
                    dorsal.appendFreqArea(x.getAllTrajectory(y).getTract()[ventralIndex - mmToTest].getResultsFile()[q].getFreqArea()[o])
                    o += 1
                q += 1

            fileIndex = x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFilesLen()
            q = 0
            while q < fileIndex:
                ventral.appendExponents(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getExponent())
                ventral.appendOffset(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getOffset())
                ventral.appendError(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getError())
                ventral.appendR2(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getR2())
                freqIndex = x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getFreqLen()
                o = 0
                while o < freqIndex:
                    ventral.appendPeakFreq(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getFreq()[o])
                    ventral.appendFreqArea(x.getAllTrajectory(y).getTract()[ventralIndex + mmToTest - 1].getResultsFile()[q].getFreqArea()[o])
                    o += 1
                q += 1
            y += 1

def getDataGreatestLength(patientArray, dorsal, ventral):
    greatest  = 0

    for x in patientArray:
        y = 0
        while y < x.getTractLen():

            tractLength = x.getAllTrajectory(y).getTractLen()
            if tractLength % 2 == 1:
                x.getAllTrajectory(y).removeTract(tractLength - 1)
                tractLength = x.getAllTrajectory(y).getTractLen()
                print('Cutout a mm from ventral to make length even for: ' +  str(x.getName()) + 'Tract ' + str(y))

            ventralIndex = tractLength // 2 #Ventral mm part starts at this index, below this index is dorsal
            if ventralIndex > greatest:
                greatest = ventralIndex
            y += 1
    return greatest
