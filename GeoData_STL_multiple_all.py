import numpy as np 
from stl import mesh 
import glob
import os

#%% READING POINT DATA
import numpy as np 
from stl import mesh 
import glob
import os
from shutil import copyfile
# # SOURCES
#path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity\\'
testPath = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\'
path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\'
corePath = path + 'centre\\'

#files_list = glob.glob(path+'*.txt')
# # TEST FILES
#files_list = glob.glob(corePath+'*.txt')
#files_list = [testPath+'679_5321t01dgm.txt', testPath+'680_5321t01dgm.txt', testPath+'681_5321t01dgm.txt']
# # REAL FILES
files_list = [path+'690_5333t01dgm.txt', path+'690_5334t01dgm.txt', path+'691_5333t01dgm.txt', path+'691_5334t01dgm.txt']
#files_list = [path+'682_5324t01dgm.txt', path+'682_5325t01dgm.txt']
#files_list = [path+'681_5324t01dgm.txt', path+'681_5325t01dgm.txt', path+'682_5324t01dgm.txt', path+'682_5325t01dgm.txt']
#files_list = [path+'681_5333t01dgm.txt', path+'681_5334t01dgm.txt', path+'682_5333t01dgm.txt', path+'682_5334t01dgm.txt', path+'683_5333t01dgm.txt', path+'683_5334t01dgm.txt']

# # SAVING: destination path and file name
storageDirectory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity_terrain\\'
saveAs = 'test8'

# # FUNCTIONS 
def get_core_files(fileList, numberOfLayers = 3, centre = (691,5334)):
    print ('collecting files around centre...')
    prefix = fileList[0][:98]
    sufix = 't01dgm.txt'
    coreFiles = []
    lowerLeftCorner = str(centre[0] - numberOfLayers) +'_' +str(centre[1] - numberOfLayers)
    firstFile = fileList.index(prefix + lowerLeftCorner + sufix)
    for stripe in range(2*numberOfLayers+1):
        startIndex = firstFile + 20*stripe
        endIndex = startIndex + (1+2*numberOfLayers)
        dim = endIndex - startIndex
        for i in range(dim):
            coreFiles.append(fileList[startIndex+i])
    print ('collected files')
    # save them in seperate folder
    for file in coreFiles:
        copyfile(file, corePath +file[-18:])
    return coreFiles, dim

def get_ring_files(fileList, numberOfLayers, coreDim, centre = (691,5334)):
    ringFiles = []
    print ('collect files of first ring')
    prefix = fileList[0][:98]
    sufix = 't01dgm.txt'
    outerDim = numberOfLayers*2+coreDim
    coreDimLayers = int((coreDim-1)/2)
    lowerLeftCorner = str(centre[0] - numberOfLayers - coreDimLayers) +'_' +str(centre[1] - numberOfLayers - coreDimLayers)
    firstFile = fileList.index(prefix + lowerLeftCorner + sufix)
    for i in range(outerDim):
        startIndex = firstFile +20*i
        if i >= numberOfLayers and i <= outerDim -numberOfLayers: 
            for s in range (2):
                for t in range (numberOfLayers):
                    ringFiles.append(fileList[startIndex+t+(s*(coreDim+numberOfLayers))])
        else:    
            for j in range(outerDim):
                ringFiles.append(fileList[startIndex+j])
    for file in ringFiles:
        copyfile(file, path + 'firstRing\\' + file[-18:])
    return ringFiles, outerDim

#core, coreDim = get_core_files(files_list, numberOfLayers=1)
#ring, ringDim = get_ring_files(files_list, 3, 7)

def transformer(fileList, xOffset = 681000, yOffset = 5324000):
    print ('setting the offsets...')
    xOffsetter = lambda x: x - xOffset
    yOffsetter = lambda x: x - yOffset
    for data in files_list:
        x = xOffsetter(np.loadtxt(data, usecols = 0))
        y = yOffsetter(np.loadtxt(data, usecols = 1))
        z = np.loadtxt(data, usecols = 2)
        #a = np.concatenate((x,y,z))
        fname = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\' + str(1)+ data[-18:] 
        np.savetxt(fname, np.c_[x,y,z], fmt="%1.2f")
        print ('transformed data')


def get_point_data_from_files(fileList):
    print ('reading point data...')
    first = True
    numberOfStripes = 1 # use for not saving everything in one big file; you have one at least

    # using usecols (0,2,4....1000)
    for files in fileList:
        if first:
            vertices = np.loadtxt(files)
            # like this all files must have the same dimension 
            xDimPatch = int(np.sqrt(len(vertices))) 
            xDim = xDimPatch
            yDim = int(np.sqrt(len(vertices)))
            first = False
        else:
            currentFileData = np.loadtxt(files)
            vertices = np.concatenate((vertices, currentFileData), axis = 0)
            # dimension of files must be quadratic also total area 
            # x direction
            if int(files[-18:-15]) == xLastPatch + 1:
                numberOfStripes +=1
                xDim += int(np.sqrt(len(currentFileData)))
            # y direction
            if int(files[-14:-10]) == yLastPatch + 1 and numberOfStripes == 1:
                yDim += int(np.sqrt(len(currentFileData)))

        # Patch means the content of one file more or less
        xLastPatch = int(files[-18:-15])
        yLastPatch = int(files[-14:-10])   

    print ('point data read')
    return vertices, xDimPatch, xDim, yDim, numberOfStripes

pointData = get_point_data_from_files(files_list)
vertices, xDimPatch, xDim, yDim, numberOfStripes = pointData[0], pointData[1], pointData[2], pointData[3], pointData[4]
#%%

#np.savetxt(corePath + 'centreAll.txt', vertices)


#%% TRIANGULATION AND STL WRITING 
import numpy as np 
from stl import mesh 

def get_points_of_outer_bounds_core(xDimPatch, yDim, numberOfStripes):
    print ('collect edge points...')
    verticalEdges = [[],[]] # right and left edge
    horizontalEdges = [[],[]] # lower and upper edge
    nodesPerStripe = xDimPatch*yDim # -1 da indices bei 0 beginnen 
    # collect vertical edge nodes right and left 
    for i in range(yDim):
        verticalEdges[0].append(i*xDimPatch)
        firstEdgeNodeRight = (numberOfStripes-1)*nodesPerStripe + xDimPatch
        verticalEdges[1].append(firstEdgeNodeRight+i*xDimPatch-1)
    # horizontal edge
    for i in range (numberOfStripes):
        for j in range (xDimPatch):
            horizontalEdges[0].append(j + i*nodesPerStripe)
            firstNodeUp = nodesPerStripe - xDimPatch
            horizontalEdges[1].append(firstNodeUp + j + i*nodesPerStripe)
    print ('collected edge points')
    return verticalEdges, horizontalEdges

def get_points_of_bounds_ring(xDimPatch, yDim, numberOfStripes, numberOfLayers, coreDim, innerFaceSize = 1, outerFaceSize = 2):
    print('collect inner edge points...')
    verticalEdges = {'outerBounds':[[],[]], 'innnerBounds': [[],[]]} # right and left edges
    horizontalEdges = {'outerBounds':[[],[]], 'innerBounds': [[],[]]} # lower and upper edges
    nodesPerStripe = xDimPatch*yDim

    # outer vertical edges
    firstOuterNodeRight = (numberOfStripes-1)*nodesPerStripe + xDimPatch - 1 - coreDim*coreDim
    for i in range(int(yDim/outerFaceSize)):
        verticalEdges['outerBounds'][0].append(i*xDimPatch*outerFaceSize)
        verticalEdges['outerBounds'][1].append(firstOuterNodeRight+i*outerFaceSize*xDimPatch)
    # inner vertical edges taking inner facesize 
    firstInnerNodeLeft = (numberOfLayers-1)*yDim + yDim*(xDimPatch-1) + numberOfLayers*xDimPatch
    firstInnerNodeRight = firstInnerNodeLeft + xDimPatch+ (2*numberOfLayers*coreDim-2)*xDimPatch
    for i in range(int((yDim-numberOfLayers*2*xDimPatch)/innerFaceSize)):
        verticalEdges['innerBounds'][0].append(firstInnerNodeLeft + i * xDimPatch*innerFaceSize)
        verticalEdges['innerBounds'][1].append(firstInnerNodeRight + i * xDimPatch*innerFaceSize)
    # outer horizontal edges
    firstOuterNodeLeft = yDim -1 
    for i in range(numberOfStripes):
        for j in range (int(xDimPatch/outerFaceSize)):
            horizontalEdges['outerBounds'][0].append(j*outerFaceSize + i*nodesPerStripe)
            horizontalEdges['outerBounds'][1].append(firstOuterNodeLeft + j*outerFaceSize + i*nodesPerStripe)
    # inner horizontal edges 
    firstInnerNodeLeftUp = firstInnerNodeLeft + coreDim
    for i in range(numberOfStripes):
        for j in range (int(xDimPatch/outerFaceSize)):
            horizontalEdges['outerBounds'][0].append(j*outerFaceSize + i*nodesPerStripe)
            horizontalEdges['outerBounds'][1].append(firstOuterNodeLeft + j*outerFaceSize + i*nodesPerStripe)

def triangulation_core(vertices, xDimPatch, xDim, yDim, numberOfStripes, faceSize): 
    print("create faces...")
    # b ___ c
    # |     |  for each two triangles
    # a ___ d
    # collect face indices in lists
    faceList = []
    #numberOfFaces = int((xDim/faceSize-1)*(yDim/faceSize-1)*2)
    xP = xDimPatch
    lastPointsXP = (xDimPatch-1)%faceSize * faceSize
    lastPointsY = (yDim-1)%faceSize * faceSize
    nextX, nextY = 0, 0
    for s in range (numberOfStripes):
        stripefactor = s*(yDim*xP) 
        for i in range (0,xDimPatch-1 - lastPointsXP, faceSize): # dimenison in x 
            for j in range (0,yDim-1 - lastPointsY , faceSize): # dimenison in y 
                a = j*xP + i + stripefactor
                b = a + xP*faceSize
                c = b + 1*faceSize 
                d = a + 1*faceSize
                faceList.append([a, b, c])
                faceList.append([a, c, d])
        nextX = xDimPatch -  lastPointsXP + stripefactor
        nextY = yDim - lastPointsY + stripefactor
        for i in range(lastPointsXP):
            for j in range(yDim -1):
                a = nextX + i + j*xP 
                b = a + xP
                c = b +1
                d = a+1
                faceList.append([a, b, c])
                faceList.append([a, c, d])
        for i in range(lastPointsY):
            for j in range(xDimPatch -1 -lastPointsXP):
                a = nextY + i + j*xP 
                b = a +xP
                c = b +1
                d = a+1
                faceList.append([a, b, c])
                faceList.append([a, c, d])
        #transition between stripes
        if s <= numberOfStripes -2:
            for i in range (0,yDim-1):
                a = i*(xP)+(xP -1) + stripefactor
                b = a + xP
                c = b + xP * (yDim-1) +1
                d = a + xP * (yDim-1) +1
                faceList.append([a, b, c]) 
                faceList.append([a, c, d])     
    
    numberOfFaces = len(faceList)
    # convert list to array
    faces = np.zeros((numberOfFaces,3), dtype=int)
    
    for i in range(numberOfFaces):
            faces[i][0] += faceList[i][0]
            faces[i][1] += faceList[i][1]
            faces[i][2] += faceList[i][2]

    return faces

def triangulation_ring(vertices, xDimPatch, xDim, yDim, outerFaceSize):
    faceList = []
    numberOfFaces = 0

def write_stl (faces, vertices):
    terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    print ('writing stl...')
    for i, f in enumerate(faces):
        for j in range(3):
            terrain.vectors[i][j] = vertices[f[j],:]
 
    print('stl written')
    return terrain

def split_and_save_stl(stlFile , filename, storageDirectory, xDimPatch, yDim, stripes, faceSize):
    maxFaces = int(2*xDimPatch/faceSize*(yDim/faceSize - 1)) #here per stripe
    # vlt hier auch noch problem mit sizes 
    stripeFactor = maxFaces
    print('splitting and saving...')
    for s in range(stripes):
        if s == stripes-1:
            maxFaces -= int(yDim/faceSize-1)*2 # no transition in the last stripe
        subTerrain = mesh.Mesh(np.zeros(maxFaces, dtype=mesh.Mesh.dtype))
        for i in range (maxFaces):
            subTerrain.vectors[i] = stlFile.vectors[i+s*stripeFactor]
        subTerrain.save(storageDirectory + filename + str(s) + '.stl')
        print ('saved:', filename + str(s) +  '.stl', 'in', storageDirectory[-27:-1])
    print ('finished') 
# # TRANSFORM DATA FROM FILES ONLY ONCE
#transformer(files_list)

#vertical, horizontal = get_points_of_outer_bounds_core( xDimPatch, yDim, numberOfStripes)
storageDirectory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity_terrain\\'

faceSize = 1
faces = triangulation_core(vertices, xDimPatch, xDim, yDim, numberOfStripes, faceSize)
print ('total faces', faces.shape[0])
print ('total stripes', numberOfStripes)

# # # CREATE MESH
terrain = write_stl(faces, vertices)
saveAs = 'test_0'
split_and_save_stl(terrain, saveAs, storageDirectory, xDimPatch, yDim, numberOfStripes, faceSize)

# %%
