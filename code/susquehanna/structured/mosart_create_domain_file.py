import os
from pyearth.system.define_global_variables import *
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pye3sm.tools.namelist.convert_namelist_to_dict import convert_namelist_to_dict

from pye3sm.mosart.mesh.structured.mosart_create_domain_1d import mosart_create_domain_1d
dResolution_meter=5000
sDate='20230329'
iCase_index_e3sm = 1
dResolution = 1/16.0
#this one should be replace 
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'
sRegion = 'susquehanna'
sMesh_type = 'mpas'

res='MOS_USRDAT'      
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'
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

sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'
aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,                                                        
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = 2005, 
                                                          iYear_end_in = 2005,
                                                          iYear_data_end_in = 1979, 
                                                          iYear_data_start_in = 1979  , 
                                                          iCase_index_in = iCase_index_e3sm, 
                                                          sDate_in = sDate, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,   
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    


oCase = pycase(aParameter_case)
sWorkspace_case_aux = oCase.sWorkspace_case_aux
sWorkspace_simulation_case_run = oCase.sWorkspace_simulation_case_run
sFilename_domain = sWorkspace_case_aux + slash + '/mosart_'+ oCase.sRegion + '_domain_mpas.nc'
if not os.path.exists(sFilename_domain):
    print(sFilename_domain + ' does not exist.')        
    sFilename_domain = sWorkspace_case_aux + slash + '/mosart_'+ oCase.sRegion + '_domain.nc' 
    if not os.path.exists(sFilename_domain):
        sFilename_mosart_in = sWorkspace_simulation_case_run + slash + 'mosart_in'
        aParameter_mosart = convert_namelist_to_dict(sFilename_mosart_in)
        sFilename_mosart_parameter = aParameter_mosart['frivinp_rtm']
        mosart_create_domain_1d(sFilename_mosart_parameter, sFilename_domain, dResolution, dResolution)
    else:
        #maybe check? this should be done in save the result
        
        pass