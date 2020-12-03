import os

rootdir = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\'
sourceDir = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\sim_domain\\'

#for file in os.walk(rootdir):
for file in os.listdir(rootdir):   
    if file [-14:] in ['5333t01dgm.txt', '5334t01dgm.txt', '5335t01dgm.txt']:
        os.rename(file, sourceDir + file)
            #os.rename (sourceDir + '\\' + file, sourceDir + subdir[-8:] + '.stl')
