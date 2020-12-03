import numpy as np
from stl import mesh
import glob

path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4. Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity_Offset\\'
files_list = glob.glob(path+'*.filepart')
totalPoints = 9*6
xP = 3
yDim = 6
xDim = 9
numberOfStripes = 3
numberperStripe = yDim*xP - xP 
print (path[:100])
#transitionId = np.arange(0, totalPoints)
#splitter = np.arange(numberperStripe, totalPoints, numberperStripe)
#first = np.split(transitionId, splitter)[0]
#middle = np.split(transitionId, splitter)[1]
#last = np.split(transitionId, splitter)[2]
startIds = list(range(yDim, yDim*xDim, yDim))
#endIds = np.arange(xP*(yDim-1), xP*(yDim-1)+ xP)
endIds = list(range(yDim -1, xDim*yDim, yDim))
# for i in range(1,numberOfStripes):
#     start = (yDim-1)*xP + endIds[-1] +1
#     end = (yDim-1)*xP + endIds[-1]+ xP +1
#     currentIds = list(range(start, end))
#     endIds.extend(currentIds)
#     #currentIds = np.arange(i*(yDim-1)*xP + endIds[-1] +1, (yDim-1)*xP + endIds[-1]+ xP +1)
#     #endIds = np.concatenate((endIds, currentIds), axis = 0)
# endIds.pop(0)
#print (startIds, endIds)



#print (b, transitionId)
# n = 5 # number of "columns"

# # collect face indices in lists
# faceList = []
# numberOfFaces = (n-1)*(n-1)*2 # total number of faces depending on number of points

# for i in range (n-1):
#     for j in range (n-1):
#         faceList.append([j*n+i, i+j*n+n, i+1+j*n+n])
#         faceList.append([j*n+i,i+1+j*n+n,j*n+1+i])

# faceMultiple =[]
# numberOfFiles = 2
# for i in range(numberOfFiles):
#     for j in range(len(faceList)): #valid for if all facelists are equal long
#         faceMultiple.append([x+(i*n*n) for x in faceList[j]])
# faces = np.zeros((numberOfFaces*numberOfFiles,3), dtype=int)
# print(faceMultiple)
# print(len(faceMultiple))
# print(len(faces))
# path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4. Master\\Hydroprojekt\\GeoData_Muc\\DTM1_MunichCity\\'
# file_name =  '_testfile.txt'#'684_5336t01dgm.txt'
# files_list = glob.glob(path+'*.txt')
# print (files_list)
# # Define the 8 vertices of the cube
# vertices = np.array([\
#     [-1.1, -1.1, -1.1],
#     [+1.1, -1.1, -1.1],
#     [+1.1, +1.1, -1.1],
#     [-1.1, +1.1, -1.1],
#     [-1.1, -1.1, +1.1],
#     [+1.1, -1.1, +1.1],
#     [+1.1, +1.1, +1.1],
#     [-1.1, +1.1, +1.1]])
# # vertices = np.array([\
# #     [-1, -1, -1],
# #     [+1, -1, -1],
# #     [+1, +1, -1],
# #     [-1, +1, -1],
# #     [-1, -1, +1],
# #     [+1, -1, +1],
# #     [+1, +1, +1],
# #     [-1, +1, +1]])
# # Define the 12 triangles composing the cube

# faces = np.array([\
#     [0,3,1],
#     [1,3,2],
#     [0,4,7],
#     [0,7,3],
#     [4,5,6],
#     [4,6,7],
#     [5,1,2],
#     [5,2,6],
#     [2,3,6],
#     [3,7,6],
#     [0,1,5],
#     [0,5,4]])
# print (type(faces[0]))
# # Create the mesh
# # cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
# # for i, f in enumerate(faces):
# #     for j in range(3):
# #         print (f[j])
# #         cube.vectors[i][j] = vertices[f[j],:]

# # # Write the mesh to file "cube.stl"
# # cube.save('cube.stl')