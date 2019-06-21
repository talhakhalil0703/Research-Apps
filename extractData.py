def extractData(patientArray, dorsal, ventral, mm):
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
                dorsal[4].append(x.getAllTrajectory(y).getTract()[z].getAverageExponent())
                dorsal[5].append(x.getAllTrajectory(y).getTract()[z].getAverageOffset())
                dorsal[6].append(x.getAllTrajectory(y).getTract()[z].getAverageR2())
                dorsal[7].append(x.getAllTrajectory(y).getTract()[z].getAverageError())
                q = 0
                while q < fileIndex:
                    dorsal[0].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getExponent())
                    dorsal[1].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getOffset())
                    dorsal[3].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getError())
                    dorsal[2].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getR2())
                    freqIndex = x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqLen()
                    o = 0
                    while o < freqIndex:
                        dorsal[8].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreq()[o])
                        dorsal[9].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqArea()[o])
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
                ventral[4].append(x.getAllTrajectory(y).getTract()[z].getAverageExponent())
                ventral[5].append(x.getAllTrajectory(y).getTract()[z].getAverageOffset())
                ventral[6].append(x.getAllTrajectory(y).getTract()[z].getAverageR2())
                ventral[7].append(x.getAllTrajectory(y).getTract()[z].getAverageError())
                q = 0
                while q < fileIndex:
                    ventral[0].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getExponent())
                    ventral[1].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getOffset())
                    ventral[3].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getError())
                    ventral[2].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getR2())
                    freqIndex = x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqLen()
                    o = 0
                    while o < freqIndex:
                        ventral[8].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreq()[o])
                        ventral[9].append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqArea()[o])
                        o += 1
                    q += 1
                z += 1
            y += 1

    print('\n'*2 + 'Ignored the first and last mm!')
    print('Done seperating into Ventral and Dorsal groups!')

