
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction



sFilename_domain_in= '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20240102001/mosart_susquehanna_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20240102001/mosart_susquehanna_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20240102001/mosart_susquehanna_parameter.geojson'
aVariable_parameter= ['nh','nt','rdep','rlen' ,'rslp', 'rwid','twid','tslp','twid','gxr','hslp']
aVariable_short= ['nh','nt','rdep','rlen' ,'rslp', 'rwid','twid','tslp','twid','gxr','hslp']
aFlag_scientific_notation_colorbar = [0,0,0,1,0,0,0,0,0,1,0]

aVariable_parameter= [ 'rdep']
aVariable_short= ['rdep']
aTitle = ['Main channel depth']
aDate_max = [0]
aDate_max = [5.00]
aUnit = ['Unit: m']
aFlag_scientific_notation_colorbar=[0]
aExtent = [-79.10236320495605, -74.35684242248536, 39.374137496948244, 42.9556583404541]
mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out, 
                                   aVariable_parameter, aVariable_short, aTitle,
                                   aFlag_scientific_notation_colorbar_in= aFlag_scientific_notation_colorbar, 
                                   aUnit_in= aUnit, aData_max_in= aDate_max, 
                                      iSize_x_in=7, iSize_y_in=8 , aExtent_in=aExtent)
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230401002/mosart_susquehanna_flow_direction_mpas.geojson'
#mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
#                                       iSize_x_in=7, iSize_y_in=8)

