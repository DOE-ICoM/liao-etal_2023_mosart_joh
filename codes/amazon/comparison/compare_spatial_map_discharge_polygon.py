import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.visual.map.vector.map_vector_polygon_file import map_vector_polygon_file
from pyearth.toolbox.management.vector.polygon_calculator import polygon_difference_cython
from pyearth.toolbox.management.vector.polygon_calculator import polygon_difference_cython_channel
from pyearth.toolbox.data.geoparquet.convert_geojson_to_geoparquet import convert_geojson_to_geoparquet
from pyearth.toolbox.management.vector.fields import retrieve_field_value
from pye3sm.mosart.general.unstructured.retrieve.mosart_retrieve_main_channel import mosart_retrieve_main_channel
from pyearth.visual.histogram.histogram_plot import histogram_plot
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
iCase_index_e3sm = 2

dResolution_meter=5000
sDate='20230501'
#this one should be replace
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

#determine the max and min from modeled results
sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'
iYear_start = 2019
iYear_end = 2019

sFilename_base='/compyfs/liao313/04model/e3sm/amazon/analysis/e3sm20240501004/river_discharge_over_land_liq/geojson/201902.geojson'
sFilename_new ='/compyfs/liao313/04model/e3sm/amazon/analysis/e3sm20240102007/river_discharge_over_land_liq/geojson/201902.geojson'
sAttribute_name_base='rive'
sAttribute_name_new='rive'
sFilename_diff='/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/amazon/comparison/discharge_difference.geojson'

#aDischarge_base = retrieve_field_value(sFilename_base,sAttribute_name_base  )
#aDischarge_new = retrieve_field_value(sFilename_new,sAttribute_name_new)

#aData_diff = retrieve_field_value(sFilename_diff,'diff')
sFilename_domain_base = '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240501004/mosart_amazon_parameter.nc'
sFilename_domain_new ='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_parameter.nc'
aChannel_base=mosart_retrieve_main_channel(sFilename_domain_base, dThreshold_in=0.01)
aChannel_new=mosart_retrieve_main_channel(sFilename_domain_new, dThreshold_in=0.01)

#polygon_difference_cython(sFilename_base, sFilename_new, sAttribute_name_base, sAttribute_name_new,  sFilename_diff,  dArea_threshold_in = 2000)

iFlag_percent = 1
if iFlag_percent == 1:
    sVar = 'perc'
    #polygon_difference_cython_channel(sFilename_base,
    #                              sFilename_new,
    #                               sAttribute_name_base,
    #                                 sAttribute_name_new,
    #                               aChannel_base,
    #                                  aChannel_new,
    #                                 sFilename_diff)

    aData_diff = retrieve_field_value(sFilename_diff, sVar)
    aData = list()
    #aData_diff[np.where(aData_diff >= 95)] = 0.0
    aData.append(aData_diff)
    print(np.mean(abs(aData_diff)))
    dMin_x= 0 #for histogram
    dMax_x = 100
    dSpace_x = 5
    dData_min  = -20
    dData_max = 20
    sUnit = r"Unit: percent"
    iFlag_scientific_notation_colorbar_in = 0
    sColormap = 'RdBu'
    sExtend = 'both'
else:
    sVar = 'diff'
    aData_diff = retrieve_field_value(sFilename_diff,sVar)
    aData_diff[np.where(aData_diff == -9999)] = 0
    aData_diff[np.where(aData_diff == 9999)] = 0.0
    aData = list()
    aData.append(aData_diff)
    print(np.mean(abs(aData_diff)))
    dMin_x = -2000
    dMax_x = 2000
    dSpace_x = 100
    dData_min = -1.0E4
    dData_max = 1.0E4
    sUnit = r"Units: ${m}^3/s$"
    iFlag_scientific_notation_colorbar_in = 1
    sColormap = 'bwr'
    sExtend = 'both'

#plot a histogram
#sFilename_out = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/amazon/comparison/discharge_difference_histogram.png'
#histogram_plot(aData,
#               sFilename_output_in = sFilename_out,
#               dMin_x_in = dMin_x,
#               dMax_x_in = dMax_x,
#               dSpace_x_in =dSpace_x,
#               iSize_x_in=12,
#               iSize_y_in=6)

#exit()

sFilename_output_png = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/amazon/comparison/discharge_difference_percent.png'

aExtent= [-80.96294746398925, -48.94024314880371, -21.183916664123537, 6.4270845413208]
#sFilename_output_png = None
sTitle = 'River discharge difference'
aLegend=list()
aLegend.append('(c)')

map_vector_polygon_file(1, sFilename_diff,
                                         sField_color_in=sVar,
                                         iFlag_scientific_notation_colorbar_in=iFlag_scientific_notation_colorbar_in,
                                         iFlag_color_in=1,
                                         iFlag_colorbar_in=1,
                                         iDPI_in = 300,
                                         dData_max_in= dData_max,
                                         dData_min_in= dData_min,
                                         sFilename_output_in=sFilename_output_png,
                                         sColormap_in = sColormap,
                                         dMissing_value_in = -9999,
                                         iFlag_zebra_in= 1,
                                         sTitle_in=sTitle,
                                         sUnit_in=sUnit,
                                         sExtend_in=sExtend,
                                            aLegend_in=aLegend,
                                         aExtent_in=aExtent)
