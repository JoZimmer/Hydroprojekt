# import all necessary modules
from mgtools import vtkViewer
from mgtools import fields
from mgtools import MGreadH5
import numpy as np
import scipy.io as sio
 
# (optional) turn on logging to print out extra information for debugging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
 
 
# define input/output filenames
vtkfilename = "velocity_field.vtk"
matfilename = "velocity_field.mat"
h5filename = "mglet_fieldgrid.h5"
 
# sliced grid? (1 for true)
# > you do not have a sliced grid - please, set to 0 (!)
islice = 0
 
# instantiate reader object with the given HDF5 filename
reader = MGreadH5(h5filename)
 
# some information about grid
NGRID = reader.fh['/RUNINFO'][-1]['NGRID']
NGRDSET = reader.fh['/RUNINFO'][-1]['NGRDSET']
 
# NB: python works with 0-based indexing like C (<-> Fortran/MATLAB) # here,
# skipping 0th-grid because it's the global grid that is sliced
if islice == 1:
  ibeg = 1
else:
  ibeg = 0
 
iend = NGRDSET # number of grid boxes

IMX = reader.fh['/GRIDS/GRIDINFO'][0]['IMX']
JMX = reader.fh['/GRIDS/GRIDINFO'][0]['JMX']
KMX = reader.fh['/GRIDS/GRIDINFO'][0]['KMX']
 
# > here {xxx,yyy,zzz} are all cells in a spatial direction on a specific LEVEL (!)
# do not consider ghost cells
# always 50 cells per box in each direction
IMX = IMX - 4
JMX = JMX - 4
KMX = KMX - 4

xstart = reader.fh['/GRIDS/GRIDINFO'][0]['X1']
xend = reader.fh['/GRIDS/GRIDINFO'][47]['X2']
ystart = reader.fh['/GRIDS/GRIDINFO'][0]['Y1']
yend = reader.fh['/GRIDS/GRIDINFO'][47]['Y2']
zstart = reader.fh['/GRIDS/GRIDINFO'][0]['Z1']
zend = reader.fh['/GRIDS/GRIDINFO'][0]['Z2']
print ('xstart: ', xstart)
print ('xend: ', xend)
# xend = 5570.0, 11570.0
# ystart, yend = 9780.0, 11780.0
# zstart, zend = 500.0, 1000.0
# > use {x,y,z}{start,end} to define the extent of your domain covered with grid on this LEVEL (!)
# (necesary because you not start from x,y,z = 0)
x = np.linspace(xstart,xend,IMX)
y = np.linspace(ystart,yend,JMX)
z = np.linspace(zstart,zend,KMX)
 
# prepare empty fields to fill (covering whole domain)
outputU = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputV = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputW = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputP = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
 
outputOmega = fields.VectorField(x=x,y=y,z=z,dtype=np.float64)
outputQ = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputLambda2 = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
 
# loop over grids (sub-domain). The finest grid at a certain place wins
for grid in range(ibeg, iend):
    # read field data
    U = reader[grid].read('U')
    V = reader[grid].read('V')
    W = reader[grid].read('W')
    P = reader[grid].read('P')
 
    # compute additional fields
    omega = fields.VectorField.vorticity(U, V, W)
    J = fields.TensorField.gradient(U, V, W)
    Q = J.Q()
    lambda2 = J.lambda2()
 
    # interpolate the data to cell-centre
    U = U.onto(P)
    V = V.onto(P)
    W = W.onto(P)
    omega = omega.onto(P)
    Q = Q.onto(P)
    lambda2 = lambda2.onto(P)
 
    # setting boundary attribute
    U.bb = P.bb
    V.bb = P.bb
    W.bb = P.bb
    omega.bb = P.bb
    Q.bb = P.bb
    lambda2.bb = P.bb
 
    # merge the data to the containers (that cover the whole domain)
    outputU.merge(U, strip=1)
    outputV.merge(V, strip=1)
    outputP.merge(P, strip=1)
    outputW.merge(W, strip=1)
    outputOmega.merge(omega, strip=1)
    outputQ.merge(Q, strip=1)
    outputLambda2.merge(lambda2, strip=1)
 
# compute velocity vector field
vel = fields.VectorField([outputU, outputV, outputW], dtype=np.float64)
 
# save processed data into classical VTK-file (NB: data duplication)
viewer = vtkViewer(name=vtkfilename, mode="binary")
viewer.write(vel, "velocity")
viewer.write(outputP, "P")
viewer.write(outputOmega, "vorticity")
viewer.write(outputQ, "Q")
viewer.write(outputLambda2, "lambda2")
viewer.close()
 
# save data into MAT-file
sio.savemat(matfilename, {'U':outputU.data, 'V':outputV.data, 'W':outputW.data, 'P':outputP.data, 'Omega':outputOmega.data, 'Q':outputQ.data, 'lambda2':outputLambda2.data, 'BP':outputBP.data})
