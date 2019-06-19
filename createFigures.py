import matplotlib.pyplot as plt
import statistics

def createFigure(name, dataPath, jitter, error, exponent,offset, rms, freqPeak, freqarea, binPeak, binArea, palpha):
    
    fig, ((off, err, r2), (peak, area, exp)) = plt.subplots(2, 3)
    err.scatter(jitter, error, alpha = palpha)
    err.set_title('Error')
    exp.scatter(jitter, exponent, alpha = palpha)
    exp.boxplot(exponent, showcaps = True, notch = True)
    print(name +': Slope median: '+ str(statistics.median(exponent)))
    exp.set_title('Slope')
    off.scatter(jitter, offset, alpha = palpha)
    off.set_title('Offset')
    y = off.boxplot(offset, showcaps = True, notch = True)
    print(name +': Offset median: '+ str(statistics.median(offset)))
    r2.scatter(jitter, rms, alpha = palpha)
    r2.set_title('R^2')
    peak.hist(freqPeak, rwidth = .9, bins = binPeak)
    peak.set_title('Peak Frequencies')
    area.hist(freqarea, rwidth = .9, bins = binArea)
    area.set_title('Freqeuncy Area')
    fig.tight_layout()
    plt.savefig(dataPath + '/' + name +'.png', transparent = False, bbox_inches = 'tight')
