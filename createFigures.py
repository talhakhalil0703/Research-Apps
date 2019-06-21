import matplotlib.pyplot as plt
import statistics
from random import uniform

def createFigure(name, dataPath, container, binPeak, binArea, palpha, average):

    jitter = []
    
    fig, ((off, err, r2), (peak, area, exp)) = plt.subplots(2, 3)
    
    if average == True:
        num = 0
        while num < len(container[7]):
            jitter.append(uniform(-0.1, 0.1))
            num += 1
        err.scatter(jitter, container[7], alpha = palpha)
        err.set_title('Error')
        exp.scatter(jitter, container[4], alpha = palpha)
        exp.boxplot(container[4], showcaps = True, notch = True)
        print(name +': Slope median: '+ str(statistics.median(container[4])))
        exp.set_title('Slope')
        off.scatter(jitter, container[5], alpha = palpha)
        off.set_title('Offset')
        off.boxplot(container[5], showcaps = True, notch = True)
        print(name +': Offset median: '+ str(statistics.median(container[5])))
        r2.scatter(jitter, container[6], alpha = palpha)
        r2.set_title('R^2')

    elif average == False:
        num = 0
        while num < len(container[3]):
            jitter.append(uniform(-0.1, 0.1))
            num += 1
        err.scatter(jitter, container[3], alpha = palpha)
        err.set_title('Error')
        exp.scatter(jitter, container[0], alpha = palpha)
        exp.boxplot(container[0], showcaps = True, notch = True)
        print(name +': Slope median: '+ str(statistics.median(container[0])))
        exp.set_title('Slope')
        off.scatter(jitter, container[1], alpha = palpha)
        off.set_title('Offset')
        off.boxplot(container[1], showcaps = True, notch = True)
        print(name +': Offset median: '+ str(statistics.median(container[1])))
        r2.scatter(jitter, container[2], alpha = palpha)
        r2.set_title('R^2')

    peak.hist(container[8], rwidth = .9, bins = binPeak)
    peak.set_title('Peak Frequencies')
    area.hist(container[9], rwidth = .9, bins = binArea)
    area.set_title('Freqeuncy Area')
    fig.tight_layout()
    plt.savefig(dataPath + '/' + name +'.png', transparent = False, bbox_inches = 'tight')
    print('Points in ' + name + ': ' + str(len(jitter)))
