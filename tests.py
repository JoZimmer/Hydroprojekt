#%% TESTS
import numpy as np 
import glob

# faceList = [0,0,0,0]
# faceList = [x+1 for x in faceList]
# a = np.arange(10)
# c = np.split(a, 5)
# storageDirectory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity\\'
path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\'
f = path +'690_5333t01dgm.txt'
files_list = glob.glob(path+'*.txt')
src = 'step1\\E_PROFIL\\'
liste = ['r0']#, 'r1', 'r2']
step = 'AU_s1_r0_e_FK.csv'
step1 = 'AU_s1_r0_e_city.csv'
step2 = 'AU_s1_r0_e_rails.csv'

x = np.arange(1,5)

print(x-1)


def get_ring_files(fileList, numberOfLayers = 1, coreDim = 3, centre = (691,5334)):
    ringFiles = [[],[],[],[]]
    print ('collect files of first ring')
    prefix = fileList[0][:98]
    sufix = 't01dgm.txt'
    outerDim = numberOfLayers*2+coreDim
    coreDimLayers = int((coreDim-1)/2) # -1 für centre dim 3 entspricht einem layer
    lowerLeftCorner = str(centre[0] - numberOfLayers - coreDimLayers) +'_' +str(centre[1] - numberOfLayers - coreDimLayers)
    firstFile = fileList.index(prefix + lowerLeftCorner + sufix)
    for i in range(outerDim):
        startIndex = firstFile + 20*i
        # horizontal files
        if i >= numberOfLayers:# and i <= outerDim - numberOfLayers:  
            for t in range (numberOfLayers+1):
                ringFiles[2].append(fileList[startIndex+t])
                ringFiles[3].append(fileList[startIndex+t+coreDim+numberOfLayers])
        # vertical files
        else:
            for s in range (numberOfLayers+1):    
                for t in range(outerDim+1):
                    ringFiles[0].append(fileList[startIndex+t + 20*s])
                    ringFiles[1].append(fileList[startIndex+20*(coreDim+1)+t +20*s])
    # ringfiles[[verticalLeft], [vertRight], [horDown], [horUp]]
    # corners are in the verticals
    return ringFiles, outerDim 



# %%
