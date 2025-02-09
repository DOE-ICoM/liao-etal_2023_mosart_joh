import numpy as np
import netCDF4 as nc #read netcdf
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

sRegion = 'amazon'
sMesh_type = 'mpas'

res='MOS_USRDAT'
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'

iCase_index_hexwatershed = 1
iCase_index_e3sm = 3

dResolution_meter=5000
sDate='20240501'
#this one should be replace
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

#determine the max and min from modeled results
sVariable = 'Main_Channel_Water_Depth_LIQ'
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
sDate_structured = '20240501'
iCase_index_e3sm_structurd = 4

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

print(dData_max)

sDate_unstructured = '20230401'
sDate_unstructured = '20240102'
iCase_index_e3sm_unstructurd = 7
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
dData_max = 40.0

#plot them separately
sUnit = r"Units: m"
sTitle = 'River water depth'
aExtent= [-80.96294746398925, -48.94024314880371, -21.183916664123537, 6.4270845413208]
aExtent_zoom = [-67.77681716624677222 , -64.78182220078018361 ,-3.45411640498741868,  -1.83608365420328745]
sColormap= 'Blues'
aLegend=list()
aLegend.append('(a)')
aLegend.append('Case 5')
mosart_map_variable_unstructured(oCase_structured,
                                 iFlag_monthly_in=1,
                                 iFlag_scientific_notation_colorbar_in=0,
                                 #iFlag_openstreetmap_in=1,
                                 dData_min_in=dData_min,
                                 dData_max_in=dData_max,
                                 sVariable_in = sVariable,
                                 sColormap_in = sColormap,
                                 #sFilename_suffix_in = '_zoom',
                                 sUnit_in= sUnit,
                                 sTitle_in=sTitle,
                                    aLegend_in=aLegend,
                                 aExtent_in = aExtent)


aLegend=list()
aLegend.append('(b)')
aLegend.append('Case 6')
mosart_map_variable_unstructured(oCase_unstructured,
                                 iFlag_monthly_in=1,
                                 iFlag_scientific_notation_colorbar_in=0,
                                 #iFlag_openstreetmap_in=1,
                                  dData_min_in=dData_min,
                                 dData_max_in=dData_max,
                                 sVariable_in = sVariable,
                                  sColormap_in = sColormap,
                                  #sFilename_suffix_in = '_zoom',
                                 sUnit_in= sUnit,
                                 sTitle_in=sTitle,
                                    aLegend_in=aLegend,
                                 aExtent_in = aExtent)
