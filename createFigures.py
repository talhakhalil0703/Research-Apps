import matplotlib.pyplot as plt
from random import uniform


def average(list):
    return sum(list) / len(list)

def createSlopeMM(name, dataPath, slopes):
    mm = []
    jitterAll = []
    slopesLen = len(slopes)
    x = 0
    jitterAmount = 0.05
    while x < slopesLen:
        mm.append(slopes[x])
        num = 0
        jitter = []
        while num < len(slopes[x]):
            jitter.append(uniform(-jitterAmount, jitterAmount))
            num += 1
        jitterAll.append(jitter)
        x += 1
    fig = plt.figure()
    mmFigure = plt.subplot()
    mmFigure.boxplot(mm, jitterAll)
    mmFigure.set_title('Slopes vs MM')
    mmFigure.set_xlabel('MM')
    mmFigure.set_ylabel('Slopes')
    plt.savefig(dataPath + '/' + name + '.png',
                transparent=False, bbox_inches='tight')

def createFigure(name, dataPath, container, binPeak, binArea, palpha, 
                average):

    jitter = []
    alphaArea = []
    betaArea = []

    fig = plt.figure(figsize=(17, 7))
    err = plt.subplot(253)
    exp = plt.subplot(251)
    off = plt.subplot(252)
    r2 = plt.subplot(258)
    peak = plt.subplot(256, xticks = [0,10,20,30,40,50,60])
    area = plt.subplot(257)
    alpha = plt.subplot(154)
    freak = plt.subplot(155, xticks = [0,10,20,30,40,50,60])
    alpha.set_ylim(bottom=0, top=13)
    scale = 1.1
    jitterAmount = 0.05
    maxc = 0.070
    minc = 0
    colorc = 'viridis'

    if average is True:
        num = 0
        while num < len(container.getAverageError()):
            jitter.append(uniform(-jitterAmount, jitterAmount))
            num += 1
        err.scatter(jitter, container.getAverageError(), alpha=palpha)
        err.axis([-0.3, 0.3, 0, max(container.getAverageError()) * scale])
        exp.scatter(jitter, container.getAverageExponents(), alpha=palpha)
        exp.axis([-0.3, 1.3, 0, 3 * scale])
        exp.boxplot(container.getAverageExponents(), showcaps=True, notch=True)
        off.scatter(jitter, container.getAverageOffset(), alpha=palpha)
        off.axis([-0.3, 1.3, 0, 8 * scale])
        off.boxplot(container.getAverageOffset(), showcaps=True, notch=True)
        r2.scatter(jitter, container.getAverageR2(), alpha=palpha)
        r2.axis([-0.3, 0.3, 0, max(container.getAverageR2()) * scale])
    elif average is False:
        num = 0
        while num < len(container.getError()):
            jitter.append(uniform(-jitterAmount, jitterAmount))
            num += 1
        err.scatter(jitter, container.getError(), alpha=palpha)
        err.axis([-0.3, 1.3, 0, max(container.getError()) * scale])
        exp.scatter(jitter, container.getExponents(), alpha=palpha)
        exp.axis([-0.3, 0.3, 0, max(container.getExponents()) * scale])
        exp.boxplot(container.getExponents(), showcaps=True, notch=True)
        off.scatter(jitter, container.getOffset(), alpha=palpha)
        off.axis([-0.3, 1.3, 0, max(container.getOffset()) * scale])
        off.boxplot(container.getOffset(), showcaps=True, notch=True)
        r2.scatter(jitter, container.getR2(), alpha=palpha)
        r2.axis([-0.3, 0.3, 0, max(container.getR2()) * scale])

    peakLen = container.getFreqLen()
    x = 0
    while x < peakLen:
        f = container.getPeakFreq()[x]
        if f >= 8 and f <= 13:
            alphaArea.append(container.getFreqArea()[x])
        elif f > 13 and f <= 35:
            betaArea.append(container.getFreqArea()[x])
        x += 1

    betaJitter = []
    alphaJitter = []
    num = 0
    while num < len(betaArea):
        betaJitter.append(uniform(-jitterAmount, jitterAmount))
        num += 1
    num = 0
    while num < len(alphaArea):
        alphaJitter.append(uniform(-jitterAmount, jitterAmount))
        num += 1
    scatter = []
    scatter.append(betaArea)
    scatter.append(alphaArea)
    jitterscatter = []
    jitterscatter.append(betaJitter)
    jitterscatter.append(alphaJitter)
    labels = ['Beta', 'Alpha']

    exp.xaxis.set_visible(False)
    off.xaxis.set_visible(False)
    r2.xaxis.set_visible(False)
    err.xaxis.set_visible(False)

    err.set_title('Error')
    off.set_title('Offset')
    exp.set_title('Slope')
    r2.set_title('R^2')

    peak.hist(container.getPeakFreq(), rwidth=.9, bins=binPeak, 
            density=True)
    peak.axis([binPeak[0], binPeak[-1], 0, 0.15])
    peak.set_title('Peak Frequencies')
    area.hist(container.getFreqArea(), rwidth=.9, bins=binArea, 
            density=True)
    area.axis([binArea[0], binArea[-1], 0, 0.45])
    area.set_title('Freqeuncy Area')
    alpha.boxplot(scatter, jitterscatter, labels=labels, showcaps=True)
    alpha.set_title('Alpha and Beta Area')
    freak.set_title('Central Frequency vs Frequency Area')
    freak.set_xlabel('Frequency')
    freak.set_ylabel('Area')
    h = plt.hist2d(container.getPeakFreq(), container.getFreqArea(), 
            bins = [binPeak, binArea], density = True, vmax = maxc, 
            vmin = minc, cmap = colorc)
    pcm = freak.pcolormesh(h[0], vmin = minc, vmax = maxc, cmap = colorc)
    plt.colorbar(pcm, ax = freak, cmap = colorc)
    freak.hist2d(container.getPeakFreq(), container.getFreqArea(), 
                bins = [binPeak, binArea], density  = True, vmax = maxc, 
                vmin = minc, cmap = colorc)
    fig.tight_layout()
    plt.savefig(dataPath + '/' + name + '.png',
                transparent=False, bbox_inches='tight')
