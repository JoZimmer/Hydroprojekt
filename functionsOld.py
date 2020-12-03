import numpy as np

def sort_Id_horizontal(vertices, xDimPatch, xDim, yDim):
    verticesSorted = []
    transitionIds = np.arange(xDimPatch-1, xDim*yDim, xDimPatch) # vector with endIDs of each row 
    lastId = np.split(transitionIds, [-yDim])[1][:-1] # letzten wert nicht da dann gar nicht mehr indexieren 
    transitionIds = np.split(transitionIds, [-yDim])[0]
    lastStripe = (xDim*yDim - yDim*xDimPatch)
    index = 0
    for i in range(yDim):
        for j in range(xDim):
            verticesSorted.append(vertices[index])
            #verticesAndIds[str(j+i*xDim)] = vertices[index]

            if index in transitionIds:
                index += xDimPatch*(yDim-1)
            elif index > lastStripe:  #damit nicht jedesmal der ganze array durchsucht wird
                if index in lastId: 
                    index = (i+1)*xDimPatch - 1 
            index +=1


    return np.asarray(verticesSorted)

def indexTable_NoBounds(indexNoBounds, dim):
    dim2 = dim - 1
    faceListNoBounds = []
    for i in range(dim2-1):
        for j in range(dim2-1):
            a = indexNoBounds[i][j]
            b = indexNoBounds[i+1][j]
            c = indexNoBounds[i+1][j+1]
            d = indexNoBounds[i][j+1]
            faceListNoBounds.append([a, b, c])
            faceListNoBounds.append([a, c, d])

    numberOfFaces = len(faceListNoBounds)
    facesNoBounds = np.zeros((numberOfFaces,3), dtype=int)
    #np.array is needed for the the stl library
    for i in range(numberOfFaces):
            facesNoBounds[i][0] += faceListNoBounds[i][0]
            facesNoBounds[i][1] += faceListNoBounds[i][1]
            facesNoBounds[i][2] += faceListNoBounds[i][2]
def triangulation_horizontal_sort(xDim, yDim): 

    # collect face indices in lists
    faceList = []
    numberOfFaces = (xDim-1)*(yDim-1)*2

    for i in range (xDim-1):
        for j in range (yDim-1):
            faceList.append([j*xDim+i, i+j*xDim+xDim, i+1+j*xDim+xDim])
            faceList.append([j*xDim+i,i+1+j*xDim+xDim,j*xDim+1+i])

    # convert list to array
    faces = np.zeros((numberOfFaces,3), dtype=int)
    
    for i in range(numberOfFaces):
            faces[i][0] += faceList[i][0]
            faces[i][1] += faceList[i][1]
            faces[i][2] += faceList[i][2]

    return faces

def split_vertices(vertices, xDimPatch, xDim, yDim, numberOfStripes):
    verticesSplit = []
    pointsPerStripe = yDim * xDimPatch + yDim
    verticesSplit.append(vertices[:pointsPerStripe])
    for i in range(1,numberOfStripes-1):
        start = i*pointsPerStripe - yDim
        end = start + pointsPerStripe
        verticesSplit.append(vertices[start:end])
    
    verticesSplit.append(vertices[-(yDim*xDimPatch):])
    return np.asarray(verticesSplit)