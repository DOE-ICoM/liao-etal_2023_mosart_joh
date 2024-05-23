import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.visual.map.vector.map_vector_polygon_data import map_vector_polygon_data
from pyearth.toolbox.management.vector.polygon_calculator import polygon_difference_rtree, polygon_difference_cython


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
sVariable = 'main_channel_water_depth_liq'
iYear_start = 2019
iYear_end = 2019

sFilename_base='/compyfs/liao313/04model/e3sm/amazon/analysis/e3sm20240501002/main_channel_water_depth_liq/geojson/201902.geojson'
sFilename_new ='/compyfs/liao313/04model/e3sm/amazon/analysis/e3sm20240102002/main_channel_water_depth_liq/geojson/201902.geojson'
sAttribute_name_base='main'
sAttribute_name_new='main'
sFilename_diff='/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/amazon/comparison/river_depth_difference.geojson'

#polygon_difference_cython(sFilename_base, sFilename_new, sAttribute_name_base, sAttribute_name_new,
#                          sFilename_diff,
#        dArea_threshold_in = 2000)

#map the sFilename_output
iFlag_scientific_notation_colorbar_in = 0
dData_min_in = -15
dData_max_in = 15

sFilename_output_png = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/amazon/comparison/river_depth_difference.png'
sVar = 'diff'
sUnit = r"Unit: m"
sTitle = 'Channel water depth difference'
aExtent= [-80.96294746398925, -48.94024314880371, -21.183916664123537, 6.4270845413208]
#sFilename_output_png = None

map_vector_polygon_data(1, sFilename_diff,
                                         sVariable_in=sVar,
                                         iFlag_scientific_notation_colorbar_in=iFlag_scientific_notation_colorbar_in,
                                         iFlag_color_in=1,
                                         iFlag_colorbar_in=1,
                                         dData_max_in= dData_max_in,
                                         dData_min_in= dData_min_in,
                                         sFilename_output_in=sFilename_output_png,
                                         sColormap_in = 'rainbow',
                                         dMissing_value_in = -9999,
                                         iFlag_zebra_in= 1,
                                         sTitle_in=sTitle,
                                         sUnit_in=sUnit,
                                         sExtend_in='both',
                                         aExtent_in=aExtent,
                                         iFlag_debug=1)
