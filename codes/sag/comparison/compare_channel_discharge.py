import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.visual.ladder.ladder_plot_xy_data import ladder_plot_xy_data
from pyearth.toolbox.management.vector.fields import retrieve_field_value
from pye3sm.mosart.general.unstructured.retrieve.mosart_retrieve_channel_from_headwater_to_outlet import mosart_retrieve_channel_from_headwater_to_outlet
from pyearth.visual.scatter.scatter_plot_multiple_data import scatter_plot_multiple_data
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
sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'
iYear_start = 2019
iYear_end = 2019

sFilename_base='/compyfs/liao313/04model/e3sm/sag/analysis/e3sm20240101001/river_discharge_over_land_liq/geojson/201908.geojson'
sFilename_new ='/compyfs/liao313/04model/e3sm/sag/analysis/e3sm20240103001/river_discharge_over_land_liq/geojson/201908.geojson'
sAttribute_name_base='rive'
sAttribute_name_new='rive'
sFilename_diff='/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/sag/comparison/discharge_difference.geojson'

sFilename_domain_base = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101001/mosart_sag_parameter.nc'
sFilename_domain_new ='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter.nc'



aDischarge_base = retrieve_field_value(sFilename_base,sAttribute_name_base )
aDischarge_new = retrieve_field_value(sFilename_new,sAttribute_name_new)

print(np.max(aDischarge_base), np.max(aDischarge_new))

aIndex_base, aLength_base, aDraiange_area_base = mosart_retrieve_channel_from_headwater_to_outlet(sFilename_domain_base, 362)
aIndex_new, aLength_new, aDraiange_area_new = mosart_retrieve_channel_from_headwater_to_outlet(sFilename_domain_new, 211)
#exit()
aLength_base = np.array(aLength_base)
aLength_new = np.array(aLength_new)

aDistance_base = np.cumsum(aLength_base[::-1])[::-1]
aDistance_new = np.cumsum(aLength_new[::-1])[::-1]

aDischarge_base = aDischarge_base[aIndex_base]
aDischarge_new = aDischarge_new[aIndex_new]


#map the sFilename_output
iFlag_scientific_notation_colorbar_in = 1
dData_min_in = -40
dData_max_in = 40

sFilename_output_png = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/sag/comparison/discharge_profile.png'

sUnit = r"Units: ${m}^3/s$"
sTitle = 'River discharge from headwater to outlet'
sFormat_x =  '%.1E'
sLabel_x = 'Distance to outlet (m)'
sLabel_y = r'River discharge (${m}^3/s$)'
aLabel_legend= ['Case 1','Case 2']

aX_all = list()
aY_all = list()

aX_all.append(aDistance_base)
aX_all.append(aDistance_new)

aDischarge_base[np.where(aDischarge_base==-9999)] = np.max(aDischarge_base)
aDischarge_new[np.where(aDischarge_new==-9999)] = np.max(aDischarge_new)

aY_all.append(aDischarge_base)
aY_all.append(aDischarge_new)
iFlag_ladder = 0

if iFlag_ladder == 1:
      ladder_plot_xy_data(aX_all,  aY_all,
        sFilename_output_png,iDPI_in = None, aFlag_trend_in = None,
            iReverse_y_in = None,  iSize_x_in = None,
                    iFlag_scientific_notation_x_in=1,
                    iFlag_scientific_notation_y_in=1,
                iSize_y_in = None,  ncolumn_in = None,
                    dMax_x_in = None,  dMin_x_in = 0,
                    dMax_y_in =500, dMin_y_in = 0,
                        dSpace_y_in = None,
                            aColor_in = ['blue','red'], aLinestyle_in = ['dotted','dashdot'],  aLinewidth_in= [1.0,1.0],
                                aLabel_point_in = None,
                                    aTick_label_x_in = None,
                                    aLocation_legend_in = [1.0,0.0],
                                        sLabel_x_in = sLabel_x,
                                        sLabel_y_in = sLabel_y,
                                            aLabel_legend_in = aLabel_legend,
        sLocation_legend_in='lower right', sFormat_x_in = sFormat_x, sFormat_y_in =None,
        sTitle_in = sTitle)


sFilename_output_png = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/codes/sag/comparison/discharge_scatterplot.png'


aData_x =list()
aData_y = list()

aDraiange_area_base = np.array(aDraiange_area_base) * 1.0E6
aDraiange_area_new = np.array(aDraiange_area_new)

aData_x.append(aDraiange_area_base)
aData_x.append(aDraiange_area_new)

aData_y.append(aDischarge_base)
aData_y.append(aDischarge_new)
iFlag_scatterplot = 1

if iFlag_scatterplot == 1:
      scatter_plot_multiple_data(aData_x,
                      aData_y,
                      sFilename_output_png,
                      iFlag_miniplot_in = 0,
                      iFlag_scientific_notation_x_in=1,
                      iFlag_scientific_notation_y_in=0,
                      iSize_x_in = None,
                      iSize_y_in = None,
                      iDPI_in = None ,
                      iFlag_log_x_in = None,
                      iFlag_log_y_in = None,
                      dMin_x_in = np.min(aDraiange_area_base),
                      dMax_x_in = np.max(aDraiange_area_base),
                      dMin_y_in = np.min(aDischarge_new),
                      dMax_y_in = np.max(aDischarge_new),
                      dSpace_x_in = None,
                      dSpace_y_in = None,
                      sFormat_x_in =None,
                      sFormat_y_in =None,
                      sLabel_x_in =r'Drainage area (${m}^2$)',
                      sLabel_y_in = 'River discharge (${m}^3/s$)' ,
                         aColor_in=['blue','red'],
                        aMarker_in=['s','h'],
                            aSize_in = None,
                      aLabel_legend_in = aLabel_legend,
                      sTitle_in = '')