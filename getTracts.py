from patientsClass import mmFile

def getTracts(start, end, all):
    tracts = []
    startIndex = all.index(start)
    endIndex = all.index(end)
    i = startIndex
    while i <= endIndex:
        mmfile = mmFile(all[i])
        tracts.append(mmfile)
        i = i + 1
    return tracts
