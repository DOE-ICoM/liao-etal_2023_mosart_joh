#this code is used to fix the error in drainage area in the DRT dataset
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.toolbox.data.beta.replace_variable_in_netcdf import replace_variable_in_netcdf

#correct the drainage area is saved in the data folder

#the old parameter file
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter.nc'

#the new parameter file
sFilename_parameter_out='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter_drainage.nc'

#we will call pyearth api to replace the drainage area in the old parameter file

#read the new dat file
sFilenew_drainage_area = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/areaTotal2_Sag_16th.dat'
dummy= text_reader_string(sFilenew_drainage_area)
aDrainage = dummy[:, 0].astype(float)

aData_in = list()
aVariable_in = list()
aData_in.append(aDrainage)
aVariable_in.append('areaTotal2')

replace_variable_in_netcdf(sFilename_parameter_in, sFilename_parameter_out, aData_in, aVariable_in)