import numpy as np
import netCDF4 as nc #read netcdf
from pyearth.system.define_global_variables import *

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


from hexwatershed_utility.mosart.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf


from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pye3sm.mosart.general.unstructured.map.mosart_map_variable_unstructured import mosart_map_variable_unstructured


iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_create_e3sm_case = 1

iFlag_mosart =1 
iFlag_elm =0 
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 0
iFlag_create_mapping_file = 1

sRegion = 'columbia'
sMesh_type = 'mpas'

res='MOS_USRDAT'      
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'

iCase_index_hexwatershed = 1
iCase_index_e3sm = 2

dResolution_meter=5000
sDate='20230501'
#this one should be replace 
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/columbia/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/columbia/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

#determine the max and min from modeled results
sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'
iYear_start = 2019
iYear_end = 2019
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
sDate_structured = '20230501'
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
for iYear in range(iYear_start, iYear_end + 1):
        sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)    
        for iMonth in range(iMonth_start, iMonth_end + 1):
            sMonth = str(iMonth).zfill(2)             
            sDate = sYear + sMonth    
            sDummy = '.mosart.h0.' + sYear + '-' + sMonth + sExtension_netcdf
            sFilename = sWorkspace_simulation_case_run + slash + sCase + sDummy     
            pDatasets = nc.Dataset(sFilename)    
            #get the variable              
            for sKey, aValue in pDatasets.variables.items():
                if sKey.lower() == sVariable.lower() :                                   
                    aData_variable = (aValue[:]).data  
                    #get fillvalue 
                    dFillvalue = float(aValue._FillValue )
                    aData_variable = aData_variable[np.where(aData_variable != dFillvalue)]
                    break
                    #save output                         
                else:
                    pass
            
            dData_max = np.max( [dData_max, np.max(aData_variable)] )
            print( np.max(aData_variable))
            


sDate_unstructured = '20230401'
iCase_index_e3sm_unstructurd = 2
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
for iYear in range(iYear_start, iYear_end + 1):
        sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)    
        for iMonth in range(iMonth_start, iMonth_end + 1):
            sMonth = str(iMonth).zfill(2)             
            sDate = sYear + sMonth    
            sDummy = '.mosart.h0.' + sYear + '-' + sMonth + sExtension_netcdf
            sFilename = sWorkspace_simulation_case_run + slash + sCase + sDummy
            pDatasets = nc.Dataset(sFilename)                           
            for sKey, aValue in pDatasets.variables.items():
                if sKey.lower() == sVariable.lower() :                                   
                    aData_variable = (aValue[:]).data                      
                    dFillvalue = float(aValue._FillValue )    
                    aData_variable = aData_variable[np.where(aData_variable != dFillvalue)]
                    break                                  
                else:
                    pass

            print( np.max(aData_variable))
            dData_max = np.max( [dData_max, np.max(aData_variable)] )
            
print(dData_max)
dData_max = 25000.0

#plot them separately
sUnit = r"${\mathrm{m}}^3/s$"
sTitle = 'River discharge over land (liquid)'
mosart_map_variable_unstructured(oCase_structured,
                                 iFlag_scientific_notation_colorbar_in=1, 
                                 dData_min_in=dData_min,
                                 dData_max_in=dData_max,
                                 sVariable_in = sVariable,
                                 sUnit_in= sUnit, 
                                 sTitle_in=sTitle)

mosart_map_variable_unstructured(oCase_unstructured,
                                 iFlag_scientific_notation_colorbar_in=1, 
                                  dData_min_in=dData_min,
                                 dData_max_in=dData_max,
                                 sVariable_in = sVariable, 
                                 sUnit_in= sUnit, 
                                 sTitle_in=sTitle)
