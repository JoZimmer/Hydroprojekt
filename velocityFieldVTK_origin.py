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
vtkfilename = "porous_rho10.vtk"
matfilename = "porous_rho10.mat"
h5filename = "mglet_fieldgrid.h5"
 
# sliced grid? (1 for true)
islice = 1
 
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
 
iend = NGRDSET
 
# read IMX etc. of global grid
IMX = reader.fh['/GRIDS/GRIDINFO'][0]['IMX']
JMX = reader.fh['/GRIDS/GRIDINFO'][0]['JMX']
KMX = reader.fh['/GRIDS/GRIDINFO'][0]['KMX']
 
# exclude ghost-cell layers (2 on each side)
IMX = IMX - 4
JMX = JMX - 4
KMX = KMX - 4
 
lx = 2.0
ly = 1.73205080756888
lz = 1.63299316185545
 
x = np.linspace(0,lx,IMX)
y = np.linspace(0,ly,JMX)
z = np.linspace(0,lz,KMX)
 
# prepare empty fields to fill
outputU = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputV = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputW = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputP = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
 
outputOmega = fields.VectorField(x=x,y=y,z=z,dtype=np.float64)
outputQ = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
outputLambda2 = fields.ScalarField(x=x,y=y,z=z,dtype=np.float64)
 
# loop over grids (sub-domain).
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
 
    # merge the data to the containers
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
