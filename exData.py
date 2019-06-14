import scipy.io as sio
content = sio.loadmat('/Users/talhakhalil/Desktop/Research/Data/2120/2120-1218auto1_fooof_results.mat')
struct = content['fooof_results']
val = struct[0,0]
print (val['background_params'])
print (val['peak_params'])
