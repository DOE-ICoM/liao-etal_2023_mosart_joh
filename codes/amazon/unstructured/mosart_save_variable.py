
import os

from pathlib import Path
from os.path import realpath

import cartopy.crs as ccrs

from pyearth.system.define_global_variables import *

from pyhexwatershed.classes.pycase import hexwatershedcase

from hexwatershed_utility.mosart.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf


from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pye3sm.mosart.general.unstructured.save.mosart_save_variable_unstructured import mosart_save_variable_unstructured
from pye3sm.mosart.general.unstructured.save.mosart_merge_variable_unstructured import mosart_merge_variable_unstructured


iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_create_e3sm_case = 1

iFlag_mosart =1
iFlag_elm =0
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 0
iFlag_create_mapping_file = 1

sRegion = 'amazon'
sMesh_type = 'mpas'

res='MOS_USRDAT'
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'

iCase_index_hexwatershed = 1
iCase_index_e3sm = 7

dResolution_meter=5000
sDate='20240102'
#this one should be replace
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/case.xml'
sModel  = 'e3sm'
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
                                                          iYear_start_in = 2019,
                                                          iYear_end_in = 2019,
                                                          iCase_index_in = iCase_index_e3sm,
                                                          sDate_in = sDate,
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )



oCase = pycase(aParameter_case)

#mosart_save_variable_unstructured(oCase, sVariable_in = sVariable, iFlag_intensity_in= 0, iFlag_monthly_in =1)

sVariable= 'Main_Channel_Water_Depth_LIQ'
#mosart_save_variable_unstructured(oCase, sVariable_in = sVariable, iFlag_intensity_in= 0, iFlag_monthly_in =1)

sVariable= 'Main_Channel_STORAGE_LIQ'
#mosart_save_variable_unstructured(oCase, sVariable_in = sVariable, iFlag_monthly_in =1)

sVariable= 'QSUR_LIQ'
mosart_save_variable_unstructured(oCase, sVariable_in = sVariable, iFlag_intensity_in =1, iFlag_monthly_in= 1)

sVariable= 'QSUB_LIQ'
mosart_save_variable_unstructured(oCase, sVariable_in = sVariable, iFlag_intensity_in =1, iFlag_monthly_in= 1)
aVariable_in = ['QSUR_LIQ', 'QSUB_LIQ']
sVariable_out = 'Q_LIQ'

mosart_merge_variable_unstructured(oCase, aVariable_in, sVariable_out, iFlag_monthly_in= 1)

sVariable= 'FLOODED_FRACTION'
#mosart_save_variable_unstructured(oCase, sVariable_in = sVariable, iFlag_resolution =1, dResolution_in=1/8.0, iFlag_intensity_in= 0, iFlag_monthly_in= 1)

