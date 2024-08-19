
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_domain.nc'

#there was an error in the structured mosart parameter file for the drainage area
#sFilename_parameter_in='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_parameter.nc'
sFilename_parameter_in='/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/inputdata/MOSART_SUS_16th_c230330.nc'

sFilename_geojson_out='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_parameter.geojson'
aVariable_parameter= ['nh','nt','rdep','rlen' ,'rslp', 'rwid','twid','tslp','twid','gxr','hslp']
aVariable_short= ['nh','nt','rdep','rlen' ,'rslp', 'rwid','twid','tslp','twid','gxr','hslp']
aFlag_scientific_notation_colorbar = [0,0,0,1,0,0,0,0,0,1,0]


aVariable_parameter= ['rwid', 'rdep']
aVariable_short= ['rwid', 'rdep']
aTitle = ['Main channel width', 'Main channel depth']
aTitle = ['', '']
aDate_max = [0, 0]
aDate_max = [800, 5.0]
aUnit = ['Unit: m', 'Unit: m']

aFlag_scientific_notation_colorbar=[0 ,0]
aFlag_colorbar = [0,0]
aColormap = ['YlGnBu', 'Blues']

aExtent = [-79.10236320495605, -74.35684242248536, 39.374137496948244, 42.9556583404541]
#aExtent = None
iFlag_parameter =1
iFlag_flow_direction = 0
if iFlag_parameter == 1:
    mosart_map_unstructured_parameters(sFilename_domain_in,
                                       sFilename_parameter_in,
                                       sFilename_geojson_out,
                                           aVariable_parameter,
                                             aVariable_short,
                                               aTitle,
                                                  aFlag_colorbar_in = aFlag_colorbar,
                                           aFlag_scientific_notation_colorbar_in= aFlag_scientific_notation_colorbar,
                                            aData_max_in= aDate_max,
                                            aColormap_in=aColormap,
                                            aUnit_in= aUnit,
                                          iSize_x_in=7,
                                          iSize_y_in=8 ,
                                          aExtent_in=aExtent)
if iFlag_flow_direction == 1:
    sFilename_geojson_out='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_flow_direction.geojson'
    mosart_map_unstructured_flow_direction(sFilename_domain_in,
                                           sFilename_parameter_in,
                                           sFilename_geojson_out,
                                       iSize_x_in=7,
                                       iSize_y_in=8,
                                          aExtent_in=aExtent)
