
#%% SET PATHS AND IMPORTS
import numpy as np 
from stl import mesh 
import glob
import os
import time
from shutil import copyfile
import matplotlib.pyplot as plt
# # SOURCES
#path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity\\'
testPath = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\'
path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\'
corePath = path + 'centre\\'
domainPath = path + 'sim_domain\\'

#files_list = glob.glob(path+'*.txt')
# # TEST FILES
#files_list = glob.glob(corePath+'*.txt')
#files_list = [testPath+'679_5321t01dgm.txt', testPath+'680_5321t01dgm.txt', testPath+'681_5321t01dgm.txt']
# # REAL FILES
files_list = glob.glob(domainPath+ '*.txt')

files_list = [path+'689_5333t01dgm.txt', path+'689_5334t01dgm.txt', #path+'687_5335t01dgm.txt', 
              path+'690_5333t01dgm.txt', path+'690_5334t01dgm.txt'] #path+'688_5335t01dgm.txt',  
              #path+'689_5333t01dgm.txt', path+'689_5334t01dgm.txt', path+'689_5335t01dgm.txt']

# # SAVING: destination path and file name
storageDirectory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\centerPatch\\'
print ('path and input set, using', len(files_list), 'files')

# TODO: for the ring files write sth that it mesh the ring stripe wise [[left], [right], [up], [down]]

#%% FINDING CERTAIN FILES

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

def read_point_data(files_list):
    t0 = time.process_time()
    print ('read data...')
    # check filesList dimension to state last row and columns
    # not necessary since no boundaries are only needed for the most outer files 
    # use list with x = 700 und y =5342 
    xList, yList = [], []
    for file in files_list:
        xList.append(int(file[-14:-10]))
        yList.append(int(file[-18:-15]))
        
    xDim, yDim = xList[-1] - xList[0] +1, yList[-1] - yList[0] +1
    
    # create fileTable to acces neigbours via indices
    fileTable = np.arange(0,len(files_list)).reshape(yDim,xDim).transpose()
    # fileTable = np.empty((xDim,yDim), dtype = int)
    # for i in range (xDim):
    #     for j in range(yDim):
    #         fileTable[j][i] = j +i*xDim
    
    vertices = []
    outerBoundsX = []
    outerBoundsY = []
    outerCorner = []
    # collect vertex data in a list and files that are the total outer bounds 
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

vertices, fileTable, outerBoundsX, outerBoundsY, outerCorner = read_point_data(files_list)

#%% FACE AND INDEX TABLE

def get_index_table(faceSize):
    
    '''
    tables with indicess which correspond to the coordinate data in the 1D array file,
    the tables however are 2D and are valid for any file 
    the boundaries are constructed by adding their coordinates to the 1D data array
    Special cases: very Last files only need one bound resp. no bound 
    Idea: add last row of points by indroducing artifical ones.. copy last row and add 1 meter
    TODO: intruduce faceSizes by modifiyng the indextables, probably delete rows and columns
    Problem here: not every faceSize fits the data of length 1001: 1,7,11,13,77
    could solve this by shifting the boundaries --> makes it ways mor difficult
    '''
    print ('create index tables...') 
    # vertexTable = np.arange(0,1001*1001).reshape(1001,1001)
    indexTableAll = np.empty((1001,1001), dtype = int)
    for i in range (1001): # starting with one to leave the first row empty
        for j in range(1000): # going to 1000 t leave the last column empty
            indexTableAll[i][j] = j + i*1000

    # boundaries
    indexTableAll[:1000,1000] = np.arange(indexTableAll[-1,-2]+1, indexTableAll[-1,-2]+1001) # right
    indexTableAll[1000, 1000] = indexTableAll[999,-1] +1 # corner

    # face Size
    indexTableFaceSize = indexTableAll[0::faceSize]
    indexTableFaceSize = indexTableFaceSize[:, ::faceSize]

    print('finished index tables with face size:', faceSize)

    return indexTableAll, indexTableFaceSize

# universal for all
def get_face_table(indexTable):
    

    '''
    same as indexTables but for faces, indexTable tables are used to acces the raw data
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

'''
possible sizes:
1,2,4,5,8,10,20,25,40,50,100,125,200,250,500
'''
faceSize = 5
# tableAll für das richtige anfügen der bounding points, 
# indexTable ist abhängig von der faceSize
indexTableAll, indexTable = get_index_table(faceSize)
# gets the modified table
faceTable = get_face_table(indexTable)

#%% TRIANGULATION AND STL WRITING

def add_points_north(patch):
    lastRow = patch[-1000:]
    northRow = np.zeros((1000,3))
    for i in range (len(lastRow)):
        northRow[i][0] += lastRow[i][0]
        northRow[i][1] += lastRow[i][1]+1
        northRow[i][2] += lastRow[i][2]
    return northRow

def add_points_west(patch):
    lastColumn = patch[999::1000]
    westColumn = np.zeros((1000,3))
    for i in range (len(lastColumn)):
        westColumn[i][0] += lastColumn[i][0]+1
        westColumn[i][1] += lastColumn[i][1]
        westColumn[i][2] += lastColumn[i][2]
    return westColumn

def triangulation(vertices, fileTable, faces, index, indexAll, outerBoundsX, outerBoundsY, outerCorner):
    # current bounds werden für tests gebraucht --> jetzt immer für äußerste
    # da eigentlich nur aller äußerste files keine übergänge haben
    bounder = 1
    currentBoundsWest, currentBoundsNorth = fileTable[:-1,-1], fileTable[-1,:-1]
    cornerBound = fileTable[-1,-1]
    if outerBoundsX and outerBoundsY:
        bounder = 0
        currentBoundsWest = outerBoundsX #!!!! geht so nicht da current inr outer str
        currentBoundsNorth = outerBoundsY
        cornerBound = outerCorner
    # wenn nur äußerste als bounds dann nehe outerBoundx, y aus read_Point_data
    
    # x bounds rechts um sich selber erweitert oben um nachbar ecke auch um sich selber
    terrainAll = []
    # acces the vertex data using the file table
    # um einfach auf die benachbarten files zu zu greifen
    for r in range(fileTable.shape[0]-bounder):
        for c in range(fileTable.shape[1]-bounder):
            t0 = time.process_time()
            print ('write faces for file', fileTable[c][r] + 1, 'of', fileTable[-1,-1]+1, '...')
            p = fileTable[c][r] # id from current file open
            patch = vertices[fileTable[c][r]] # point data of current patch
           
            # case: file hat nur nördliche Nachbarn also befindet sich am rechten rand
            if p in currentBoundsWest:
                north = vertices[fileTable[c+1][r]][indexAll[0,:-1]]
                west = add_points_west(patch)
                corner = west[-1].reshape(1,3)
                corner[0][1] += 1
            # case: letzte reihe, also nur westliche nachbarn
            elif p in currentBoundsNorth:
                north = add_points_north(patch)
                west = vertices[fileTable[c][r+1]][indexAll[:-1,0]]
                corner = west[-1].reshape(1,3)
                corner[0][1] += 1

            # case: letzte ecke braucht künstliche nachbarn nord UND west
            elif p == cornerBound:
                north = add_points_north(patch)
                west =  add_points_west(patch)
                corner = west[-1].reshape(1,3)
                corner[0][1] += 1
            # case: nachbar nord und west: nehme punkte der angrenzenden files
            else:
                north = vertices[fileTable[c+1][r]][indexAll[0,:-1]]
                west = vertices[fileTable[c][r+1]][indexAll[:-1,0]]
                corner = vertices[fileTable[c+1][r+1]][indexAll[0,0]].reshape(1,3)
            
            # bounds added to the 1D point data array
            patch = np.concatenate((patch, north, west, corner), axis =0)
            #np.savetxt('C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity_terrain\\centre\\'+str(fileTable[c][r])+'.txt', patch)
            terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            t0 = time.process_time()
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
    
    print('saving...')
    filenames = []
    for i in range(fileTable.shape[0]-1):
        for j in range (fileTable.shape[1]-1):
            filenames.append(files_list[fileTable[j][i]])
    for s, stl in enumerate(stlFilesList):
        stl.save(storageDirectory + 'Geo_' + filenames[s][-18:-10] + '_'+ str(faceSize)+'.stl')
        print ('saved:', 'Geo_' + filenames[s][-18:-10] + '_'+ str(faceSize)+  '.stl', 'in', storageDirectory[-26:-1])
    print ('finished')


stlList = triangulation(vertices, fileTable, faceTable, indexTable, indexTableAll, outerBoundsX, outerBoundsY, outerCorner)
save_stl(stlList, files_list, fileTable, storageDirectory, faceSize)
# %%
