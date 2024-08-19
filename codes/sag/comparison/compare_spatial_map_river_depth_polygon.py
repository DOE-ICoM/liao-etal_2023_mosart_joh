import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.visual.map.vector.map_vector_polygon_data import map_vector_polygon_data
from pyearth.toolbox.management.vector.polygon_calculator import polygon_difference_cython, polygon_difference_cython_channel
from pyearth.toolbox.data.geoparquet.convert_geojson_to_geoparquet import convert_geojson_to_geoparquet
from pye3sm.mosart.general.unstructured.retrieve.mosart_retrieve_main_channel import mosart_retrieve_main_channel
from pyearth.toolbox.management.vector.fields import retrieve_field_value
iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_create_e3sm_case = 1

iFlag_mosart =1
iFlag_elm =0
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 0
iFlag_create_mapping_file = 1

sRegion = 'sag'
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
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

#determine the max and min from modeled results
sVariable = 'main_channel_water_depth_liq'
iYear_start = 2019
iYear_end = 2019

sFilename_base='/compyfs/liao313/04model/e3sm/sag/analysis/e3sm20240101002/main_channel_water_depth_liq/geojson/201908.geojson'
sFilename_new ='/compyfs/liao313/04model/e3sm/sag/analysis/e3sm20240103001/main_channel_water_depth_liq/geojson/201908.geojson'
sAttribute_name_base='main'
sAttribute_name_new='main'
sFilename_diff='/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/sag/comparison/river_depth_difference.geojson'
sFilename_domain_base = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter.nc'
sFilename_domain_new ='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter.nc'
aChannel_base=mosart_retrieve_main_channel(sFilename_domain_base, dThreshold_in=0.05)
aChannel_new=mosart_retrieve_main_channel(sFilename_domain_new, dThreshold_in=0.05)


#polygon_difference_cython(sFilename_base,
#                              sFilename_new,
#                               sAttribute_name_base,
#                                 sAttribute_name_new,
#                                  sFilename_diff,
#                                  iFlag_percent_in=iFlag_percent)
iFlag_percent = 1
if iFlag_percent == 1:
    sVar = 'perc'
    polygon_difference_cython_channel(sFilename_base,
                                  sFilename_new,
                                   sAttribute_name_base,
                                     sAttribute_name_new,
                                   aChannel_base,
                                      aChannel_new,
                                      sFilename_diff)
    
    aData_diff = retrieve_field_value(sFilename_diff, sVar)

    aData_diff[np.where(aData_diff >= 95)] = 0.0
    aData_diff[np.where(aData_diff <= -95)] = 0.0
    print(np.mean(abs(aData_diff)))

    dData_min = -20.0
    dData_max = 20.0
    sUnit = r"Unit: percent"
    iFlag_scientific_notation_colorbar_in = 0
    sColormap = 'RdBu'
    sExtend = 'both'
else:
    sVar = 'diff'
    polygon_difference_cython_channel(sFilename_base,
                                  sFilename_new,
                                   sAttribute_name_base,
                                     sAttribute_name_new,
                                   aChannel_base,
                                      aChannel_new,
                                      sFilename_diff)

    aData_diff = retrieve_field_value(sFilename_diff, sVar)
    aData_diff[np.where(aData_diff == -9999)] = 0
    aData_diff[np.where(aData_diff == 9999)] = 0.0



#sFilename_parquet = sFilename_diff.replace('.geojson', '.parquet')
#convert_geojson_to_geoparquet(sFilename_diff , sFilename_parquet)

sFilename_output_png = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/sag/comparison/river_depth_difference_percent.png'


sTitle = 'Water depth difference'
aExtent = [-150.015625, -146.234375, 67.921875, 70.328125]

map_vector_polygon_data(1, sFilename_diff,
                                         sVariable_in=sVar,
                                         iFlag_scientific_notation_colorbar_in=iFlag_scientific_notation_colorbar_in,
                                         iFlag_colorbar_in=1,
                                         iFlag_color_in = 1,
                                         iFlag_zebra_in=1,
                                         iDPI_in= 300,
                                         dData_max_in= dData_max,
                                         dData_min_in= dData_min,
                                         sFilename_output_in=sFilename_output_png,
                                         sColormap_in = sColormap,
                                         dMissing_value_in = -9999,
                                         sTitle_in=sTitle,
                                         sUnit_in=sUnit,
                                         sExtend_in='both',
                                         aExtent_in=aExtent,
                                         iFlag_debug=0)
