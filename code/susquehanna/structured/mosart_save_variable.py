
import os

from pathlib import Path
from os.path import realpath

import cartopy.crs as ccrs

from pyearth.system.define_global_variables import *

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
from pyhexwatershed.classes.pycase import hexwatershedcase


from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pye3sm.mosart.general.unstructured.save.mosart_save_variable_unstructured import mosart_save_variable_unstructured





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


mosart_save_variable_unstructured( oCase, sVariable_in = sVariable)

sVariable= 'Main_Channel_STORAGE_LIQ'
mosart_save_variable_unstructured(oCase, sVariable_in = sVariable)

sVariable= 'Main_Channel_Water_Depth_LIQ'
mosart_save_variable_unstructured(oCase, sVariable_in = sVariable)