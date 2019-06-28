def storeExcelData(Patient, workBook):
    trajectory = Patient.getTractLen()
    x = 0
    while x < trajectory:
        sheet = workBook.create_sheet(
            str(Patient.getName()) + ' Tract ' + str(x))
        Patient.getAllTrajectory(x)
        slope = []
        offset = []
        error = []
        r2 = []
        peak = []
        area = []
        trajectoryLen = Patient.getAllTrajectory(x).getTractLen()
        y = 0
        while y < trajectoryLen:
            slope.append(Patient.getAllTrajectory(
                x).getTract()[y].getAverageExponent())
            offset.append(Patient.getAllTrajectory(
                x).getTract()[y].getAverageOffset())
            r2.append(Patient.getAllTrajectory(x).getTract()[y].getAverageR2())
            error.append(Patient.getAllTrajectory(
                x).getTract()[y].getAverageError())
            fileLen = Patient.getAllTrajectory(
                x).getTract()[y].getResultsFilesLen()
            z = 0
            while z < fileLen:
                peak.append(Patient.getAllTrajectory(x).getTract()
                            [y].getResultsFile()[z].getFreq())
                area.append(Patient.getAllTrajectory(x).getTract()
                            [y].getResultsFile()[z].getFreqArea())
                z += 1
            y += 1
        length = len(slope)
        sheet['A1'] = 'Slope'
        sheet['B1'] = 'Offset'
        sheet['C1'] = 'Error'
        sheet['D1'] = 'R2'
        sheet['E1'] = 'Peak'
        sheet['F1'] = 'Area'
        y = 0
        q = 0
        while y < length:
            sheet['A' + str(y + 2)] = slope[y]
            sheet['B' + str(y + 2)] = offset[y]
            sheet['C' + str(y + 2)] = error[y]
            sheet['D' + str(y + 2)] = r2[y]
            z = 0
            length2 = len(peak[y])
            while z < length2:
                sheet['E' + str(q + 2)] = peak[y][z]
                sheet['F' + str(q + 2)] = area[y][z]
                q += 1
                z += 1
            y += 1
        x += 1
