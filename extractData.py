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


