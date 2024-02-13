
import os


from pyearth.system.define_global_variables import *

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file



from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pye3sm.mesh.unstructured.e3sm_convert_unstructured_domain_file_to_scripgrid_file import e3sm_convert_unstructured_domain_file_to_scripgrid_file
from pye3sm.mesh.e3sm_create_structured_envelope_domain_file_1d import e3sm_create_structured_envelope_domain_file_1d
from pye3sm.mesh.e3sm_create_mapping_file import e3sm_create_mapping_file
from pye3sm.mesh.e3sm_map_domain_files import e3sm_map_domain_files
from pye3sm.mosart.general.structured.remap.mosart_remap_variable_structured import mosart_remap_variable_structured

iCase_index_e3sm = 1
sRegion = 'susquehanna'
sMesh_type = 'mpas'
res='MOS_USRDAT'      
compset = 'RMOSGPCC'
project = 'esmd'
sDate='20230329'
sModel  = 'e3sm'
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/case.xml'

sWorkspace_scratch = '/compyfs/liao313'
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
                                                          iYear_start_in = 1980, 
                                                          iYear_end_in = 2019,                                                         
                                                          iCase_index_in = iCase_index_e3sm, 
                                                          sDate_in = sDate, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,   
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    


oCase = pycase(aParameter_case)

#we need to create a mapping file between two cases

#convert elm to script file         

sWorkspace_output = oCase.sWorkspace_case_aux
sFilename_mosart_unstructured_domain = '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230401006/mosart_susquehanna_domain.nc'
sFilename_mosart_unstructured_script = '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230401006/mosart_susquehanna_scriptgrid.nc'

sFilename_elm_structured_domain_file_out_1d = '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_domain.nc'
sFilename_elm_structured_script_1d = sWorkspace_output + '/elm_susquehanna_scripgrid_latlon.nc'

sFilename_map_elm_to_mosart = sWorkspace_output + slash + 'susquehanna_mapping.nc'
e3sm_convert_unstructured_domain_file_to_scripgrid_file(sFilename_elm_structured_domain_file_out_1d, sFilename_elm_structured_script_1d )   
    
#convert mosart to script file  

e3sm_create_mapping_file( sFilename_elm_structured_script_1d, sFilename_mosart_unstructured_script , sFilename_map_elm_to_mosart )

mosart_remap_variable_structured( oE3SM, oCase, sFilename_map_elm_to_mosart)

