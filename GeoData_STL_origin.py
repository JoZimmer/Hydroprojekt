import numpy as np 
from stl import mesh 
import glob

# # PREQUESITES: 
# - DTM files must have the same amount of points in x and y direction (quadtratic)
# - all files in the list must have the same amount of points

# # SOURCES
path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4. Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity\\'
#files_list = glob.glob(path+'*.txt')
#files_list = [path+'_testfile.txt', path+'_testfile1.txt']
files_list = [path+'684_5336t01dgm.txt']#, path+'681_5325t01dgm.txt']

# # SAVING
directory = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4. Master\\Hydroprojekt\\GeoData_Muc\\STL_MunichCity\\'
saveAs = 'Munich3.stl'
#saveAs = 'testAll.stl'

# # FUNCTONS 

def assemble_faces_by_indices(numberOfFaces,terrainDimenson):

    # collect face indices in lists
    faceList = []
    n = terrainDimenson
    for i in range (n-1):
        for j in range (n-1):
            faceList.append([j*n+i, i+j*n+n, i+1+j*n+n])
            faceList.append([j*n+i,i+1+j*n+n,j*n+1+i])
    
    # convert lists to arrays 
    faces = np.zeros((numberOfFaces,3), dtype=int)
    for i in range(numberOfFaces):
            faces[i][0] += faceList[i][0]
            faces[i][1] += faceList[i][1]
            faces[i][2] += faceList[i][2]
    return faces

# # MESH

# initialize mesh(stl) for all files
meshDimenson = int(np.sqrt(len(np.loadtxt(files_list[0])))) 
numberOfFaces = (meshDimenson-1)*(meshDimenson-1)*2
numberOfFiles = len(files_list)
terrain = mesh.Mesh(np.zeros(numberOfFaces*numberOfFiles, dtype=mesh.Mesh.dtype)) 

# fill the stl file
totalFaces = 0
for n, fileName in enumerate(files_list):


    vertices = np.loadtxt(fileName)
    faces = assemble_faces_by_indices(numberOfFaces,meshDimenson)

    totalFaces += faces.shape[0] #only for counting faces
    
    for i, f in enumerate(faces):
        for j in range(3):
            terrain.vectors[i+n*numberOfFaces][j] = vertices[f[j],:]

    transition = vertices[-meshDimenson:]
# save
terrain.save(directory + saveAs)
print ('total faces:', totalFaces)
print('saved:' , directory + saveAs)
