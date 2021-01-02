import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
import DIN_wind_profiles
import pandas as pd

'''
some examples to test the direct reading from the mglet_fieldgrid hdf file
'''

rootDir = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\simulations\\'
sourceFile = rootDir + 'step1\\refinement0\\9000_nt\\mglet_fieldgrid.h5'

fileKeys =  ['FIELDS', 'GRIDS', 'RUNINFO']
fieldKeys = ['AGGM_LVL01', 'AG_LVL01', 'APPM_LVL01', 'AP_LVL01', 'ASSM_LVL01', 'AUUM_LVL01', 
             'AUVM_LVL01', 'AUWM_LVL01', 'AU_LVL01', 'AVVM_LVL01', 'AVWM_LVL01', 'AV_LVL01', 
             'AWWM_LVL01', 'AW_LVL01', 'BP_LVL01', 'G_LVL01', 'P_LVL01', 'U_LVL01', 'V_LVL01', 'W_LVL01']

resultFile = h5.File(sourceFile, 'r')
fields = resultFile['FIELDS']
grids = resultFile['GRIDS']
variable = 'AU_LVL01'
z = 'Z_LVL01'
x = 'X_LVL01'

fieldValue = fields[variable]
gridBox = 37
cellsX = 50
cellsY = 2
start = 54*cellsX * cellsY + 2 # 2 für ghost layers
end = start + 51

linePlotValues = fieldValue[gridBox][start:end]
z = np.arange(0,len(linePlotValues)*10,10) #10 m height per cell --> 
# TODO: take this value directly form the h5 file

# # DIN
category = 'IV'
vb = 10
v_z,Iv_z, z_din = DIN_wind_profiles.plot_DIN(vb, category)

fig = plt.figure('linePlot '+ variable)
ax = fig.add_subplot(111)
ax.plot(linePlotValues, z, '-')
ax.set_xlabel(variable)
ax.set_ylabel('z [m]')

ax.plot(v_z/10, z_din, label = 'DIN - category '+category)
# ax1.set_xlabel(' Iv(z), v(z)/v_ref')
# ax1.set_ylabel('z/z_ref')
# ax1.legend()
# ax1.grid()
plt.grid()
plt.show()
