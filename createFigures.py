import matplotlib.pyplot as plt
from random import uniform

def average(list):
    return sum(list)/len(list)

def createFigure(name, dataPath, container, binPeak, binArea, palpha, average):

    jitter = []
    
    fig, ((off, err, r2), (peak, area, exp)) = plt.subplots(2, 3)
    
    if average == True:
        num = 0
        while num < len(container.getAverageError()):
            jitter.append(uniform(-0.1, 0.1))
            num += 1
        err.scatter(jitter, container.getAverageError(), alpha = palpha)
        err.set_title('Error')
        exp.scatter(jitter, container.getAverageExponents(), alpha = palpha)
        exp.boxplot(container.getAverageExponents(), showcaps = True, notch = True)
        print(name +': Slope median: '+ str(sum(container.getAverageExponents())/len(container.getAverageExponents())))
        exp.set_title('Slope')
        off.scatter(jitter, container.getAverageOffset(), alpha = palpha)
        off.set_title('Offset')
        off.boxplot(container.getAverageOffset(), showcaps = True, notch = True)
        print(name +': Offset median: '+ str(sum(container.getAverageOffset())/len(container.getAverageOffset())))
        r2.scatter(jitter, container.getAverageR2(), alpha = palpha)
        r2.set_title('R^2')

    elif average == False:
        num = 0
        while num < len(container.getError()):
            jitter.append(uniform(-0.1, 0.1))
            num += 1
        err.scatter(jitter, container.getError(), alpha = palpha)
        err.set_title('Error')
        exp.scatter(jitter, container.getExponents(), alpha = palpha)
        exp.boxplot(container.getExponents(), showcaps = True, notch = True)
        print(name +': Slope median: '+ str(sum(container.getExponents())/len(container.getExponents())))
        exp.set_title('Slope')
        off.scatter(jitter, container.getOffset(), alpha = palpha)
        off.set_title('Offset')
        off.boxplot(container.getOffset(), showcaps = True, notch = True)
        print(name +': Offset median: '+ str(sum(container.getOffset())/len(container.getOffset())))
        r2.scatter(jitter, container.getR2(), alpha = palpha)
        r2.set_title('R^2')


    peak.hist(container.getPeakFreq(), rwidth = .9, bins = binPeak, density = True)
    peak.axis([binPeak[0], binPeak[-1], 0, 0.06])
    peak.set_title('Peak Frequencies')
    area.hist(container.getFreqArea(), rwidth = .9, bins = binArea, density = True)
    area.axis([binArea[0], binArea[-1], 0, 0.65])
    area.set_title('Freqeuncy Area')
    fig.tight_layout()
    plt.savefig(dataPath + '/' + name +'.png', transparent = False, bbox_inches = 'tight')
    print('Points in ' + name + ': ' + str(len(jitter)))
