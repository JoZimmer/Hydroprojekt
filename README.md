Python scripts that were written in the context of a study project:
LES of atmospheric flow over city terrain

- DTM_to_STL.py: 
To create .stl files from rastered point clouds from a digital terrain model (DTM)

- wind_profile_from_csv.py: 
For plotting wind field data. Data source are csv files generated by the linePlot function in Paraview.

- DIN_wind_profiles.py: 
Funtions to plot mean wind speed and turbulence intensity profiles according to DIN EN 1991 - 1-4. Depending on the terrain category and the basis wind speed velocity.

- velocityFieldVTK_s1-3.py: 
Generates a 3D velocity field from the mglet_fieldgrid.h5 result file in vtk format. s1-s3 are hard coded versions that are needed for different domain sizes. certain indices differ (from line 49 on). --> maybe this can be done in a generic way by finding these accroding indices in the hdf file.

- rename_Geo_to_body.py: 
Renames geodata files such as they are required in MGLET

- hdf_postprocessing.py: 
Some tests to directly read data from the mglet_fieldgrid.h5 result file (never used, only testings)
