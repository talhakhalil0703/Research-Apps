import matplotlib.pyplot as plt
from random import uniform

def average(list):
    return sum(list)/len(list)

def createFigure(name, dataPath, container, binPeak, binArea, palpha, average):

    jitter = []
    alphaArea = []
    betaArea = []

    fig = plt.figure(figsize= (10,7))
    err = plt.subplot(243)
    exp = plt.subplot(241)
    off = plt.subplot(242)
    r2 = plt.subplot(247)
    peak = plt.subplot(246)
    area = plt.subplot(245)
    alpha = plt.subplot(144)
    scale = 1.1

    if average == True:
        num = 0
        while num < len(container.getAverageError()):
            jitter.append(uniform(-0.1, 0.1))
            num += 1
        err.scatter(jitter, container.getAverageError(), alpha = palpha)
        err.axis([-0.3, 0.3, 0, max(container.getAverageError())* scale])
        err.set_title('Error')
        exp.scatter(jitter, container.getAverageExponents(), alpha = palpha)
        exp.axis([-0.3, 0.3, 0, max(container.getAverageExponents())* scale])
        exp.boxplot(container.getAverageExponents(), showcaps = True, notch = True)
        exp.set_title('Slope')
        off.scatter(jitter, container.getAverageOffset(), alpha = palpha)
        off.axis([-0.3, 0.3, 0, max(container.getAverageOffset())* scale])
        off.set_title('Offset')
        off.boxplot(container.getAverageOffset(), showcaps = True, notch = True)
        r2.scatter(jitter, container.getAverageR2(), alpha = palpha)
        r2.axis([-0.3, 0.3, 0, max(container.getAverageR2())* scale])
        r2.set_title('R^2')

    elif average == False:
        num = 0
        while num < len(container.getError()):
            jitter.append(uniform(-0.1, 0.1))
            num += 1
        err.scatter(jitter, container.getError(), alpha = palpha)
        err.axis([-0.3, 0.3, 0, max(container.getError()) * scale])
        err.set_title('Error')
        exp.scatter(jitter, container.getExponents(), alpha = palpha)
        exp.axis([-0.3, 0.3, 0, max(container.getExponents())* scale])
        exp.boxplot(container.getExponents(), showcaps = True, notch = True)
        exp.set_title('Slope')
        off.scatter(jitter, container.getOffset(), alpha = palpha)
        off.axis([-0.3, 0.3, 0, max(container.getOffset())* scale])
        off.set_title('Offset')
        off.boxplot(container.getOffset(), showcaps = True, notch = True)
        r2.scatter(jitter, container.getR2(), alpha = palpha)
        r2.axis([-0.3, 0.3, 0, max(container.getR2())* scale])
        r2.set_title('R^2')

    peakLen = container.getFreqLen()
    x = 0
    while x < peakLen:
        f = container.getPeakFreq()[x]
        if f >= 8 and f<= 13:
            alphaArea.append(container.getFreqArea()[x])
        elif f > 13 and f <= 35:
            betaArea.append(container.getFreqArea()[x])
        x += 1

    betaJitter = []
    alphaJitter = []
    num = 0
    while num < len(betaArea):
        betaJitter.append(uniform(-0.1, 0.1))
        num += 1
    num = 0
    while num < len(alphaArea):
        alphaJitter.append(uniform(-0.1, 0.1))
        num += 1
    scatter = []
    scatter.append(betaArea)
    scatter.append(alphaArea)
    jitterscatter = []
    jitterscatter.append(betaJitter)
    jitterscatter.append(alphaJitter)
    labels = ['Beta' , 'Alpha']
    peak.hist(container.getPeakFreq(), rwidth = .9, bins = binPeak, density = True)
    peak.axis([binPeak[0], binPeak[-1], 0, 0.06])
    peak.set_title('Peak Frequencies')
    area.hist(container.getFreqArea(), rwidth = .9, bins = binArea, density = True)
    area.axis([binArea[0], binArea[-1], 0, 0.65])
    area.set_title('Freqeuncy Area')
    alpha.boxplot(scatter, jitterscatter, labels = labels, showcaps = True)
    alpha.set_title('Alpha and Beta')
    fig.tight_layout()
    plt.savefig(dataPath + '/' + name +'.png', transparent = False, bbox_inches = 'tight')

