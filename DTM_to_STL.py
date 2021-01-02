
#%% SET PATHS AND IMPORTS
import numpy as np 
from stl import mesh 
import glob
import os
import time
from shutil import copyfile
import matplotlib.pyplot as plt
# # SOURCES
# TODO: get away from absolute pathes
testPath = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\'
path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\'
corePath = path + 'centre\\'
domainPath = path + 'sim_domain\\'

#files_list = glob.glob(path+'*.txt')
# # TEST FILES
#files_list = glob.glob(corePath+'*.txt')
#files_list = [testPath+'679_5321t01dgm.txt', testPath+'680_5321t01dgm.txt', testPath+'681_5321t01dgm.txt']
# # REAL FILES
files_list = glob.glob(domainPath + '*.txt') # all files 

'''
in this files_list all files plus the direct bounding files must be included.
boudning means the file with data north, west and the corner of the terrain that should be covered. 
The example below thus created the stl file of only the first entry of this list. 
'''
files_list = [path+'689_5333t01dgm.txt', path+'689_5334t01dgm.txt', #path+'687_5335t01dgm.txt', 
              path+'690_5333t01dgm.txt', path+'690_5334t01dgm.txt'] #path+'688_5335t01dgm.txt',  
              #path+'689_5333t01dgm.txt', path+'689_5334t01dgm.txt', path+'689_5335t01dgm.txt']

# # SAVING: destination path 
storageDirectory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\centerPatch\\'
print ('path and input set, using', len(files_list), 'files')


#%% FINDING CERTAIN FILES
'''
can be used if a circular refinement is introduced
--> files around a centre are selected 
but is never used here
'''

def get_core_files(fileList, numberOfLayers = 2, centre = (691,5334)):
    print ('collecting files around centre...')
    prefix = fileList[0][:98]
    sufix = 't01dgm.txt'
    coreFiles = []
    lowerLeftCorner = str(centre[0] - numberOfLayers) +'_' +str(centre[1] - numberOfLayers)
    firstFile = fileList.index(prefix + lowerLeftCorner + sufix)
    for stripe in range(2*numberOfLayers+2):
        startIndex = firstFile + 20*stripe
        endIndex = startIndex + (1+2*numberOfLayers)
        dim = endIndex - startIndex
        for i in range(dim+1):
            coreFiles.append(fileList[startIndex+i])
    print ('collected files')
    return coreFiles, dim

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

#%% READING POINT DATA

'''
from the list of files the data of the points in the DTM files is read
a lookup table is created that sorts the given files in to a rectangle according to the dimensons in x and y
that is coverd by the given files
'''

def read_point_data(files_list):
    t0 = time.process_time()
    print ('read data...')
    
    # the dimensons are calculated from the string the files
    xList, yList = [], []
    for file in files_list:
        xList.append(int(file[-14:-10]))
        yList.append(int(file[-18:-15]))
        
    xDim, yDim = xList[-1] - xList[0] +1, yList[-1] - yList[0] +1
    
    # create fileTable to acces neigbours via indices
    # this is done since the files with the data is saved in a 1D array 
    # TODO: maybe directly collect the files in a 2D array
    fileTable = np.arange(0,len(files_list)).reshape(yDim,xDim).transpose()
    
    # collect vertex data in a list and files that are the total outer bounds
    # the outer files are identified by their coordinates 
    vertices = []
    outerBoundsX = []
    outerBoundsY = []
    outerCorner = []
    for file in files_list:
        vertices.append(np.loadtxt(file))
        if int(file[-14:-10]) == 5343 and int(file[-18:-15]) == 700:
            outerCorner.append(file)
        elif int(file[-14:-10]) == 5343:
            outerBoundsX.append(file)
        elif int(file[-18:-15]) == 700:
            outerBoundsY.append(file)
        
    #outer Files
    print ('data read in',  round(time.process_time()-t0,3), 's')
    return vertices, fileTable, outerBoundsX, outerBoundsY, outerCorner

# function call 
vertices, fileTable, outerBoundsX, outerBoundsY, outerCorner = read_point_data(files_list)

#%% FACE AND INDEX TABLE

'''
lookup tables with indices are generated that map a the data of 1D arrays to 2D arrays. 
These are needed to generate a mesh 
'''

def get_index_table(faceSize):
    
    '''
    Tables with indices which correspond to the coordinate data in the 1D array file.
    The tables however are 2D and are valid for any file. 
    The boundaries are constructed using the neigbouhring files by adding their coordinates to the 1D data array
    Special cases: very Last files only need one bound resp. no bound 
    Idea: add last row of points by indroducing artifical points.. copy last row/column and add 1 meter
    '''
    print ('create index tables...') 
    # vertexTable = np.arange(0,1001*1001).reshape(1001,1001)
    indexTableAll = np.empty((1001,1001), dtype = int)
    for i in range (1001): 
        for j in range(1000): # going to 1000 t leave the last column empty
            indexTableAll[i][j] = j + i*1000

    # boundaries
    indexTableAll[:1000,1000] = np.arange(indexTableAll[-1,-2]+1, indexTableAll[-1,-2]+1001) # right
    indexTableAll[1000, 1000] = indexTableAll[999,-1] +1 # corner

    # introducing the face siz by only keeping the i th and row and column
    indexTableFaceSize = indexTableAll[0::faceSize]
    indexTableFaceSize = indexTableFaceSize[:, ::faceSize]

    print('finished index tables with face size:', faceSize)

    return indexTableAll, indexTableFaceSize

def get_face_table(indexTable):

    '''
    Same as indexTables but for faces. 
    IndexTable tables are used to acces the raw data:
    The indices of the data points the form a triangle are extracted from the table with all indices
    '''

    print ('write face tables...')
    t0 = time.process_time()

    # 1. bounds north, west and corner
    dim = indexTable.shape[0]
    
    faceList = []
    # b ___ c
    # |     |  for each two triangles
    # a ___ d
    for i in range(dim-1):
        for j in range(dim-1):
            a = indexTable[i][j]
            b = indexTable[i+1][j]
            c = indexTable[i+1][j+1]
            d = indexTable[i][j+1]
            faceList.append([a, b, c])
            faceList.append([a, c, d])

    numberOfFaces = len(faceList)
    faces = np.zeros((numberOfFaces,3), dtype=int)

    #np.array is needed for the the stl library
    for i in range(numberOfFaces):
            faces[i][0] += faceList[i][0]
            faces[i][1] += faceList[i][1]
            faces[i][2] += faceList[i][2]

    print ('finished face table in:', round(time.process_time()-t0,3), 's')
    return faces

# # FUNCTION CALLS
'''
possible face sizes:
1,2,4,5,8,10,20,25,40,50,100,125,200,250,500
'''
faceSize = 5
# tableAll: for the bounding points, 
# indexTable: dependent on face size
indexTableAll, indexTable = get_index_table(faceSize)
# gets the modified table
faceTable = get_face_table(indexTable)

#%% TRIANGULATION AND STL WRITING
'''
The raw data of the DTM files is written to stl format
'''

def add_points_north(patch):
    '''
    auxiliary function to add an artifical row in the north 
    '''
    lastRow = patch[-1000:]
    northRow = np.zeros((1000,3))
    for i in range (len(lastRow)):
        northRow[i][0] += lastRow[i][0]
        northRow[i][1] += lastRow[i][1]+1
        northRow[i][2] += lastRow[i][2]
    return northRow

def add_points_west(patch):
    '''
    auxiliary function to add an artifical column in the west
    '''
    lastColumn = patch[999::1000]
    westColumn = np.zeros((1000,3))
    for i in range (len(lastColumn)):
        westColumn[i][0] += lastColumn[i][0]+1
        westColumn[i][1] += lastColumn[i][1]
        westColumn[i][2] += lastColumn[i][2]
    return westColumn

def triangulation(vertices, fileTable, faces, index, indexAll, outerBoundsX, outerBoundsY, outerCorner):
    '''
    from the raw vertex data a list of stl files is generated by using a python library.
    This library returns an object of type mesh that has all the information stl files need. 
    the face_table is used to assign the correct points to the respective vectors.
    '''
    # collect the files that are the bounds of the current settings
    bounder = 1 # needed to distinguish if files are most outer bounds
    currentBoundsWest, currentBoundsNorth = fileTable[:-1,-1], fileTable[-1,:-1]
    cornerBound = fileTable[-1,-1]
    # check if the files that are the most outer bounds are present
    if outerBoundsX and outerBoundsY:
        bounder = 0
        currentBoundsWest = outerBoundsX #!!!! geht so nicht da current in outer str
        currentBoundsNorth = outerBoundsY
        cornerBound = outerCorner
    
    terrainAll = []

    # acces the vertex data using the file table
    for r in range(fileTable.shape[0]-bounder):
        for c in range(fileTable.shape[1]-bounder):
            t0 = time.process_time()
            print ('write faces for file', fileTable[c][r] + 1, 'of', fileTable[-1,-1]+1, '...')
            p = fileTable[c][r] # id from current file open
            patch = vertices[fileTable[c][r]] # point data of current patch
           
            # case: file only has neigbours to the right --> located at the north bound
            if p in currentBoundsWest:
                north = vertices[fileTable[c+1][r]][indexAll[0,:-1]]
                west = add_points_west(patch)
                corner = west[-1].reshape(1,3)
                corner[0][1] += 1
            # case: last row --> only neighbours to the west
            elif p in currentBoundsNorth:
                north = add_points_north(patch)
                west = vertices[fileTable[c][r+1]][indexAll[:-1,0]]
                corner = west[-1].reshape(1,3)
                corner[0][1] += 1

            # case: the file is the outer corner
            elif p == cornerBound:
                north = add_points_north(patch)
                west =  add_points_west(patch)
                corner = west[-1].reshape(1,3)
                corner[0][1] += 1

            # case (normal): neighbour to the north and west exists
            else:
                north = vertices[fileTable[c+1][r]][indexAll[0,:-1]]
                west = vertices[fileTable[c][r+1]][indexAll[:-1,0]]
                corner = vertices[fileTable[c+1][r+1]][indexAll[0,0]].reshape(1,3)
            
            # add bounds to the current patch
            patch = np.concatenate((patch, north, west, corner), axis =0)

            #np.savetxt('C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity_terrain\\centre\\'+str(fileTable[c][r])+'.txt', patch)
            terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            problemCounter = 0
            for i, f in enumerate(faces):
                for j in range(3):
                    try:
                        terrain.vectors[i][j] = patch[f[j],:]
                    except IndexError:
                        problemCounter +=1
                        #print ('IndexProblem:',f)

            terrainAll.append(terrain)
            print('stl written in:', round(time.process_time()-t0,3), 's')
            print (problemCounter, 'problems')
    return terrainAll

def save_stl(stlFilesList, filesList, fileTable, storageDirectory, faceSize):
    '''
    save all stl files given in a list. 
    the naming of the files is done accroding to the coordinates of the files and the face size used.
    '''
    print('saving...')
    filenames = []
    for i in range(fileTable.shape[0]-1):
        for j in range (fileTable.shape[1]-1):
            filenames.append(files_list[fileTable[j][i]])
    for s, stl in enumerate(stlFilesList):
        stl.save(storageDirectory + 'Geo_' + filenames[s][-18:-10] + '_'+ str(faceSize)+'.stl')
        print ('saved:', 'Geo_' + filenames[s][-18:-10] + '_'+ str(faceSize)+  '.stl', 'in', storageDirectory[-26:-1])
    print ('finished')

# Function Calls
stlList = triangulation(vertices, fileTable, faceTable, indexTable, indexTableAll, outerBoundsX, outerBoundsY, outerCorner)
save_stl(stlList, files_list, fileTable, storageDirectory, faceSize)
# %%
