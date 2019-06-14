import scipy.io as sio
import matplotlib.pyplot as plt
content = sio.loadmat('/Users/talhakhalil/Desktop/Research/Data/2120/2120-1218auto1_fooof_results.mat')
struct = content['fooof_results']
val = struct[0,0]
exponential = val['background_params'][0][1]
error = val['error'][0][0]
r2 = val['r_squared'][0][0]
peak = val['peak_params']
peakvalues = []
for x in peak:
    peakvalues.append(x[0])

#plt.scatter(0,error)
#plt.show()
print(exponential)
print(error)
print(r2)
print(peakvalues)
#print (val['background_params'])
#print (val['peak_params'])
