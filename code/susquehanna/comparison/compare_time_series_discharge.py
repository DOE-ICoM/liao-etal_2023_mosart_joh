import os
import numpy as np
import netCDF4 as nc #read netcdf
from datetime import datetime
import glob
from pyearth.system.define_global_variables import *
from pyearth.visual.timeseries.plot_time_series_data import plot_time_series_data
from pyearth.toolbox.data.nwis.retrieve_nwis_discharge import retrieve_nwis_discharge

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


from hexwatershed_utility.mosart.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf


from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pyearth.toolbox.date.day_in_month import day_in_month
import pyearth.toolbox.date.julian as julian
current_file_path = os.path.abspath(__file__)
print(current_file_path)
current_file_directory = os.path.dirname(current_file_path)
print(current_file_directory)
iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_create_e3sm_case = 1

iFlag_mosart =1 
iFlag_elm =0 
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 0
iFlag_create_mapping_file = 1

sRegion = 'susquehanna'
sMesh_type = 'mpas'

res='MOS_USRDAT'      
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'

iCase_index_hexwatershed = 1
iCase_index_e3sm = 1

dResolution_meter=5000
sDate='20230329'
#this one should be replace 
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

#determine the max and min from modeled results
sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'

    


aDate= list()
iYear_start = 2018
iYear_end = 2019
for iYear in range(iYear_start,iYear_end+1):
    for iMonth in range(1,13):
        #get day count in this month
        iDay_end = day_in_month(iYear, iMonth)
        for iDay in range(1,iDay_end+1):            
            aDate.append(datetime(iYear,iMonth,iDay))

aDate = np.array(aDate)
nDay = len(aDate)
aParameter_e3sm = pye3sm_read_e3sm_configuration_file(sFilename_e3sm_configuration ,\
                                                          iFlag_debug_in = 0, \
                                                          iFlag_branch_in = 0,\
                                                          iFlag_continue_in = 0,\
                                                          iFlag_resubmit_in = 0,\
                                                          iFlag_short_in = 0 ,\
                                                          RES_in =res,\
                                                         Project_in = project,\
                                                          COMPSET_in = compset)
oE3SM = pye3sm(aParameter_e3sm)

#read structure mosart result
sDate_structured = '20230329'
iCase_index_e3sm_structurd = 1

dData_min = 0
dData_max = -9999
aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,                                                        
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = iYear_start, 
                                                          iYear_end_in = iYear_end,                                                        
                                                          iCase_index_in = iCase_index_e3sm_structurd, 
                                                          sDate_in = sDate_structured, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,   
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    


oCase_structured = pycase(aParameter_case)
sWorkspace_analysis_case = sWorkspace_analysis_case = oCase_structured.sWorkspace_analysis_case
sWorkspace_simulation_case_run = oCase_structured.sWorkspace_simulation_case_run
sCase = oCase_structured.sCase
iMonth_start = 1
iMonth_end = 12
id_structure  = 2
aData_structured = np.full(nDay, np.nan, dtype= float)
#find out cell index 
sWorkspace_case_aux = oCase_structured.sWorkspace_case_aux
sFilename_parameter = sWorkspace_case_aux + slash + '/mosart_'+ oCase_structured.sRegion + '_parameter.nc'
pDatasets_parameter = nc.Dataset(sFilename_parameter, 'r')
pDimension = pDatasets_parameter.dimensions.keys()
for sKey, aValue in pDatasets_parameter.variables.items():            
    if (sKey.lower() == 'id'):                   
        aData_id = (aValue[:]).data
        continue
cell_index = np.where(aData_id == id_structure)

for iYear in range(iYear_start, iYear_end + 1):
    sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)            
    sDate = sYear + '*'    
    sPattern = '*.mosart.h1.' + sDate + sExtension_netcdf
    sFilepaths = sWorkspace_simulation_case_run + slash + sPattern
    aFilenames =  glob.glob(sFilepaths, recursive = False)
    iCount = len(aFilenames)
    if iCount ==1 :            
        sFilename = aFilenames[0]
        #sFilename = sWorkspace_simulation_case_run + slash + sCase + sDummy     
        pDatasets = nc.Dataset(sFilename)    
        #get the variable              
        for sKey, aValue in pDatasets.variables.items():
            if sKey.lower() == sVariable.lower() :                                   
                aData_variable = (aValue[:]).data  
                #get fillvalue 
                dFillvalue = float(aValue._FillValue )                          
                pass                            
        #deal with daily data
        ndays = len(aData_variable)
        #convert the first day to julian day
        dummy1 = datetime(iYear, 1, 1)
        lJulian_start = julian.to_jd(dummy1, fmt='jd')
        for i in range(0,ndays):
            juilian_day = int(lJulian_start  + i +0.5 )
            pd  = julian.from_jd(juilian_day, fmt='jd')   
            mon =  pd.month
            day = pd.day
            dateobj = datetime(iYear,mon,day)
            lIndex = np.where(aDate == dateobj)
            #print(aData_variable[i, cell_index])
            aData_structured[lIndex] = aData_variable[i, cell_index]
    else:
        print('data is missing')    
        
            


sDate_unstructured = '20230401'
iCase_index_e3sm_unstructurd = 1
aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,                                                        
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = iYear_start, 
                                                          iYear_end_in = iYear_end,                                                        
                                                          iCase_index_in = iCase_index_e3sm_unstructurd, 
                                                          sDate_in = sDate_unstructured, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,   
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    


oCase_unstructured = pycase(aParameter_case)
sWorkspace_analysis_case = sWorkspace_analysis_case = oCase_unstructured.sWorkspace_analysis_case
sWorkspace_simulation_case_run = oCase_unstructured.sWorkspace_simulation_case_run
sCase = oCase_unstructured.sCase
id_unstructured  = 152663 #150382
sWorkspace_case_aux = oCase_unstructured.sWorkspace_case_aux
sFilename_parameter = sWorkspace_case_aux + slash + '/mosart_'+ oCase_unstructured.sRegion + '_parameter_mpas.nc'
pDatasets_parameter = nc.Dataset(sFilename_parameter, 'r')
pDimension = pDatasets_parameter.dimensions.keys()
for sKey, aValue in pDatasets_parameter.variables.items():            
    if (sKey.lower() == 'cellid'):                   
        aData_id = (aValue[:]).data
        continue
cell_index = np.where(aData_id == id_unstructured)
aData_unstructured = np.full(nDay, np.nan, dtype= float)
for iYear in range(iYear_start, iYear_end + 1):
    sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)            
    sDate = sYear + '*'    
    sPattern = '*.mosart.h1.' + sDate + sExtension_netcdf
    sFilepaths = sWorkspace_simulation_case_run + slash + sPattern
    aFilenames =  glob.glob(sFilepaths, recursive = False)
    iCount = len(aFilenames)
    if iCount ==1 :            
        sFilename = aFilenames[0]
        #sFilename = sWorkspace_simulation_case_run + slash + sCase + sDummy     
        pDatasets = nc.Dataset(sFilename)                              
        for sKey, aValue in pDatasets.variables.items():
            if sKey.lower() == sVariable.lower() :                                   
                aData_variable = (aValue[:]).data                      
                dFillvalue = float(aValue._FillValue )                    
           
        #deal with daily data
        ndays = len(aData_variable)
        #convert the first day to julian day
        dummy1 = datetime(iYear, 1, 1)
        lJulian_start = julian.to_jd(dummy1, fmt='jd')
        for i in range(0,ndays):
            juilian_day = int(lJulian_start  + i +0.5 )
            pd  = julian.from_jd(juilian_day, fmt='jd')   
            mon =  pd.month
            day = pd.day
            dateobj = datetime(iYear,mon,day)
            lIndex = np.where(aDate == dateobj)
            #print(aData_variable[i, cell_index])
            aData_unstructured[lIndex] = aData_variable[i, cell_index]
            

#use a plotter to visualize the data

#now read the usgs
sSite= '01578310'

dummy = retrieve_nwis_discharge(sSite, iYear_start,1,1, iYear_end, 12, 31)
cfs2cms = 0.028316847
aDischarge_obs= dummy[0] * cfs2cms

sFilename_out = current_file_directory + slash + 'streamflow_comparison.png'
plot_time_series_data( [aDate, aDate, aDate], [aDischarge_obs, aData_structured, aData_unstructured], 
                      sFilename_out = sFilename_out,
                      iFlag_scientific_notation_in = 1,
                      aLabel_legend_in=['Observation','1/16 DRT-based','MPAS-based'],
                        aColor_in=['black','red','blue'],
                          aLinestyle_in=['solid','solid','solid'],
                            aMarker_in=['None','None','None'],  )


