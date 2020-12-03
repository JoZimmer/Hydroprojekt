import os
import shutil

rootdir =   'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\GeoData_for_Simulation\\0\\'
sourceDir = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\GeoData_for_Simulation\\1\\'

#for file in os.walk(rootdir):
i = 1
for file in os.listdir(rootdir):  
    if i < 10:
        os.rename(rootdir + file, sourceDir + 'body.00'+ str(i) +'.stl')
        i+=1
    else:
        os.rename(rootdir + file, sourceDir + 'body.0'+ str(i) +'.stl')
        i+=1
    # elif file[0] == '6':
    #     os.rename(rootdir + file, sourceDir + 'body.'+ file[-11:-9] + file[-5] +'.stl')
