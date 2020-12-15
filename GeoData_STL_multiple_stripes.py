import numpy as np 
from stl import mesh 
import glob

# # SOURCES
path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity\\'
testPath = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\'
#files_list = glob.glob(path+'*.txt')
# # TEST FILES
#files_list = glob.glob(testPath+'*.txt')
#files_list = [testPath+'679_5320t01dgm.txt', testPath+'679_5321t01dgm.txt', testPath+'680_5320t01dgm.txt', testPath+'680_5321t01dgm.txt']
#files_list = [testPath+'679_5320t01dgm.txt', testPath+'679_5321t01dgm.txt']
# # REAL Files
#files_list = [path+'682_5324t01dgm.txt', path+'682_5325t01dgm.txt']
files_list = [path+'681_5333t01dgm.txt', path+'681_5334t01dgm.txt', path+'682_5333t01dgm.txt', path+'682_5334t01dgm.txt', path+'683_5333t01dgm.txt', path+'683_5334t01dgm.txt']

# # SAVING: destination path and file name
storageDirectory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4.Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity\\'
#saveAs = 'Munich2.stl'
saveStartStripe = 100
saveAs = 681_5324 #.stl'

# # FUNCTIONS 
def get_point_data_from_files(fileList):

    first = True
    numberOfStripes = 1 # use for not saving everything in one big file; you have one at least

    for files in fileList:
        if first:
            vertices = np.loadtxt(files)
            # like this all files must have the same dimension 
            xDimPatch = int(np.sqrt(len(vertices))) #for indexing for triangulation
            xDim = xDimPatch
            yDim = int(np.sqrt(len(vertices)))
            first = False
        else:
            currentFileData = np.loadtxt(files)
            vertices = np.concatenate((vertices, currentFileData), axis = 0)
            # dimension of files must be quadratic also total area 
            if int(files[-18:-15]) == xLastPatch + 1:
                numberOfStripes +=1
                xDim += int(np.sqrt(len(currentFileData)))
            if int(files[-14:-10]) == yLastPatch + 1 and numberOfStripes == 1:
                yDim += int(np.sqrt(len(currentFileData)))

        # Patch means the content of one file more or less
        xLastPatch = int(files[-18:-15])
        yLastPatch = int(files[-14:-10])    

    return vertices, xDimPatch, xDim, yDim, numberOfStripes

def sort_Id_vertical(vertices, xDimPatch, xDim, yDim):
    verticesSorted = []
    print ('soring vertices...')
    # list with ids of points in first row
    startIds = list(range(0, xDimPatch))
    for i in range(1,numberOfStripes):
        start = (yDim-1)*xDimPatch + startIds[-1] +1
        end = (yDim-1)*xDimPatch + startIds[-1]+ xDimPatch +1
        currentIds = list(range(start, end))
        startIds.extend(currentIds) 
    startIds.pop(0) #dont have to do a switch in the last column
    # vector with endIDs of each column
    endIds = list(range(xDimPatch*(yDim-1), xDimPatch*(yDim-1)+ xDimPatch))
    for i in range(1,numberOfStripes):
        start = (yDim-1)*xDimPatch + endIds[-1] +1
        end = (yDim-1)*xDimPatch + endIds[-1]+ xDimPatch +1
        currentIds = list(range(start, end))
        endIds.extend(currentIds) 
    endIds.pop(-1)

    index = 0
    for i in range(xDim):
        for j in range(yDim):
            verticesSorted.append(vertices[index])

            #if index in endIds:
            if index == endIds[0]: #--> when poping always the first one after using it 
                index = startIds[endIds.index(index)] - xDimPatch
                endIds.pop(index) # --> remove used index to fasten the search
            index += xDimPatch
    print ('vertices sorted')
    return np.asarray(verticesSorted)

def triangulation_with_transition(xDimPatch, xDim, yDim, numberOfStripes): 

    # collect face indices in lists
    faceList = []
    numberOfFaces = (xDim-1)*(yDim-1)*2
    transition = False
    
    for s in range (numberOfStripes):
        stripefactor = s*((yDim-1)*xDimPatch + xDimPatch)
        if not transition:
            for i in range (xDimPatch-1): # dimenison in x 
                for j in range (yDim-1): # dimenison in y 
                    a = j*(xDimPatch) + i + stripefactor
                    b = i+xDimPatch*(1+j) + stripefactor
                    c = i+1+xDimPatch*(1+j) + stripefactor
                    d = i+1+j*xDimPatch + stripefactor
                    faceList.append([a, b, c])
                    faceList.append([a, c, d])
            transition = True
        if transition:
            for i in range (yDim-1):
                a = i*(xDimPatch)+(xDimPatch -1) + stripefactor
                b = a + xDimPatch + stripefactor
                c = b + xDimPatch * (yDim-1) +1 + stripefactor
                d = a + xDimPatch * (yDim-1) +1 + stripefactor
                faceList.append([a, b, c]) 
                faceList.append([a, c, d])     
            transition = False   

    # convert list to array
    faces = np.zeros((numberOfFaces,3), dtype=int)
    
    for i in range(numberOfFaces):
            faces[i][0] += faceList[i][0]
            faces[i][1] += faceList[i][1]
            faces[i][2] += faceList[i][2]

    return faces

def triangulation_vertical_sort(xDim, yDim): 

    # collect face indices in lists
    faceList = []
    numberOfFaces = (xDim-1)*(yDim-1)*2

    for i in range (xDim-1):
        for j in range (yDim-1):
            a = j + yDim*i
            b = j + 1 + yDim*i
            c = b + yDim
            d = a + yDim
            faceList.append([a, b, c])
            faceList.append([a, c, d])

    # convert list to array
    faces = np.zeros((numberOfFaces,3), dtype=int)
    
    for i in range(numberOfFaces):
            faces[i][0] += faceList[i][0]
            faces[i][1] += faceList[i][1]
            faces[i][2] += faceList[i][2]

    return faces

def write_stl(faces, vertices, storageDirectory, saveStartStripe):
    # split first
    #pointsPerStripe = yDim * xDimPatch + yDim
    facesPerStripe = (yDim-1) * xDimPatch * 2 #including transition
    #verticeSplitter = np.arange(pointsPerStripe, xDim*yDim, pointsPerStripe)
    faceSplitter = np.arange(facesPerStripe, faces.shape[0], facesPerStripe)

    #verticesStripes = split_vertices(vertices, xDimPatch, xDim, yDim, numberOfStripes)
    faceStripes = np.split(faces, faceSplitter)

    for stripNumber, strip in enumerate(faceStripes):
        terrain = mesh.Mesh(np.zeros(strip.shape[0], dtype=mesh.Mesh.dtype))
        print ('writing stl...')
        for i, f in enumerate(strip):
            for j in range(3):
                terrain.vectors[i][j] = vertices[f[j],:]
  
        terrain.save(storageDirectory + str(saveStartStripe + stripNumber) + '_5324-43.stl')
        print ('saved:', str(saveStartStripe +  stripNumber) + '_5324-43.stl', 'in', storageDirectory[-27:-1])


# # GET DATA FROM FILES AND TRIANGULATION
print ('reading point data...')
pointData = get_point_data_from_files(files_list)
vertices, xDimPatch, xDim, yDim, numberOfStripes = pointData[0], pointData[1], pointData[2], pointData[3], pointData[4]
print ('point data read')

# # SORT VERTICES ARRAY 

#vertices = sort_Id_vertical(vertices, xDimPatch, xDim, yDim)

# # WRITE FACES
print ('create faces...')
faces = triangulation_with_transition(xDimPatch, xDim, yDim, numberOfStripes)
#faces = triangulation_vertical_sort(xDim, yDim)
print ('total faces', faces.shape[0])
print ('total stripes', numberOfStripes)

# # CREATE MESH
write_stl(faces, vertices, storageDirectory, saveAs)