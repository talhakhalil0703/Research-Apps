import matplotlib.pyplot as plt
from random import uniform

def create_slope_mm(name, data_path, slopes):
    mm = []
    jitter_all = []
    slopes_len = len(slopes)
    jitter_amount = 0.05
    x = 0
    while x < slopes_len:
        mm.append(slopes[x])
        num = 0
        jitter = []
        while num < len(slopes[x]):
            jitter.append(uniform(-jitter_amount, jitter_amount))
            num += 1
        jitter_all.append(jitter)
        x += 1
    fig = plt.figure()
    mm_figure = plt.subplot()
    mm_figure.boxplot(mm, jitter_all)
    mm_figure.set_title(name + ' vs MM')
    mm_figure.set_xlabel('MM')
    mm_figure.set_ylabel(name)
    plt.savefig(data_path + '/' + name + '.png', bbox_inches = 'tight')

def create_figure(name, data_path, container, bin_peak, bin_area, palpha):
    jitter = []
    alpha_area = []
    beta_area = []

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
    jitter_amount = 0.05
    maxc = 0.070
    minc = 0
    colorc = 'viridis'
    num = 0
    while num < len(container.average_error):
        jitter.append(uniform(-jitter_amount, jitter_amount))
        num += 1
    err.scatter(jitter, container.average_error, alpha=palpha)
    err.axis([-0.3, 0.3, 0, max(container.average_error) * scale])
    exp.scatter(jitter, container.average_exponents, alpha=palpha)
    exp.axis([-0.3, 1.3, 0, 3 * scale])
    exp.boxplot(container.average_exponents, showcaps=True, notch=True)
    off.scatter(jitter, container.average_offset, alpha=palpha)
    off.axis([-0.3, 1.3, 0, 8 * scale])
    off.boxplot(container.average_offset, showcaps=True, notch=True)
    r2.scatter(jitter, container.average_r2, alpha=palpha)
    r2.axis([-0.3, 0.3, 0, max(container.average_r2) * scale])
    peak_len = len(container.peak_freq)
    x = 0
    while x < peak_len:
        f = container.peak_freq[x]
        if f >= 8 and f <= 13:
            alpha_area.append(container.freq_area[x])
        elif f > 13 and f <= 35:
            beta_area.append(container.freq_area[x])
        x += 1

    beta_jitter = []
    alpha_jitter = []

    num = 0
    while num < len(beta_area):
        beta_jitter.append(uniform(-jitter_amount, jitter_amount))
        num += 1
    num = 0
    while num < len(alpha_area):
        alpha_jitter.append(uniform(-jitter_amount, jitter_amount))
        num += 1

    scatter = []
    scatter.append(beta_area)
    scatter.append(alpha_area)
    jitter_scatter = []
    jitter_scatter.append(beta_jitter)
    jitter_scatter.append(alpha_jitter)
    labels = ['Beta', 'Alpha']

    exp.xaxis.set_visible(False)
    off.xaxis.set_visible(False)
    r2.xaxis.set_visible(False)
    err.xaxis.set_visible(False)

    err.set_title('Error')
    off.set_title('Offset')
    exp.set_title('Slope')
    r2.set_title('R^2')

    peak.hist(container.peak_freq, rwidth=.9, bins=bin_peak,
            density=True)
    peak.axis([bin_peak[0], bin_peak[-1], 0, 0.15])
    peak.set_title('Peak Frequencies')
    area.hist(container.freq_area, rwidth=.9, bins=bin_area,
            density=True)
    area.axis([bin_area[0], bin_area[-1], 0, 0.45])
    area.set_title('Freqeuncy Area')
    alpha.boxplot(scatter, jitter_scatter, labels=labels, showcaps=True)
    alpha.set_title('Alpha and Beta Area')
    freak.set_title('Central Frequency vs Frequency Area')
    freak.set_xlabel('Frequency')
    freak.set_ylabel('Area')
    h = plt.hist2d(container.peak_freq, container.freq_area,
            bins = [bin_peak, bin_area], density = True, vmax = maxc,
            vmin = minc, cmap = colorc)
    pcm = freak.pcolormesh(h[0], vmin = minc, vmax = maxc, cmap = colorc)
    plt.colorbar(pcm, ax = freak, cmap = colorc)
    freak.hist2d(container.peak_freq, container.freq_area,
                bins = [bin_peak, bin_area], density  = True, vmax = maxc,
                vmin = minc, cmap = colorc)
    fig.tight_layout()
    plt.savefig(data_path + '/' + name + '.png',
                transparent=False, bbox_inches='tight')
