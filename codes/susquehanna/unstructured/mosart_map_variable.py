


from pyearth.system.define_global_variables import *

from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

from pye3sm.mosart.general.unstructured.map.mosart_map_variable_unstructured import mosart_map_variable_unstructured


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
iCase_index_e3sm = 6

dResolution_meter=5000
sDate='20230401'
#this one should be replace
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/case.xml'
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
                                                          iYear_start_in = 2005,
                                                          iYear_end_in = 2005,
                                                          iYear_data_dlnd_end_in = 1979,
                                                          iYear_data_dlnd_start_in = 2009  ,
                                                          iCase_index_in = iCase_index_e3sm,
                                                          sDate_in = sDate,
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )



oCase = pycase(aParameter_case)
sUnit = r"${\mathrm{m}}^3/s$"

sTitle = 'River discharge over land (liquid)'
mosart_map_variable_unstructured(oCase, sVariable_in = sVariable, sUnit_in= sUnit, sTitle_in=sTitle,iFlag_scientific_notation_colorbar_in=1)

sVariable= 'Main_Channel_STORAGE_LIQ'
sUnit = r"${\mathrm{m}}^3$"
sTitle = 'Main channel storage (liquid)'
mosart_map_variable_unstructured(oCase, sVariable_in = sVariable, sUnit_in= sUnit, sTitle_in=sTitle,iFlag_scientific_notation_colorbar_in=1)

sVariable= 'Main_Channel_Water_Depth_LIQ'
sUnit = r"{\mathrm{m}}"
sTitle = 'Main channel water depth (liquid)'
mosart_map_variable_unstructured(oCase, sVariable_in = sVariable, sUnit_in= sUnit, sTitle_in=sTitle,iFlag_scientific_notation_colorbar_in=0)

sVariable= 'QSUR_LIQ'
sUnit = r"${\mathrm{m}}^3$"
sTitle = 'Surface runoff (liquid)'
mosart_map_variable_unstructured(oCase, sVariable_in = sVariable, sUnit_in= sUnit, sTitle_in=sTitle,iFlag_scientific_notation_colorbar_in=1)

sVariable= 'QSUB_LIQ'
sUnit = r"${\mathrm{m}}^3$"
sTitle = 'Subsurface runoff (liquid)'
#mosart_map_variable_unstructured(oCase, sVariable_in = sVariable, sUnit_in= sUnit, sTitle_in=sTitle,iFlag_scientific_notation_colorbar_in=1)