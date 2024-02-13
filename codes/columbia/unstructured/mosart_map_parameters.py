
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction



sFilename_domain_in= '/compyfs/liao313/04model/e3sm/columbia/cases_aux/e3sm20230401002/mosart_columbia_domain_mpas.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/columbia/cases_aux/e3sm20230401002/mosart_columbia_parameter_mpas.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/columbia/cases_aux/e3sm20230401002/mosart_columbia_parameter_mpas.geojson'


mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out, 
                                      iSize_x_in=8, iSize_y_in=8)
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/columbia/cases_aux/e3sm20230401002/mosart_columbia_flow_direction_mpas.geojson'
mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                       iSize_x_in=8, iSize_y_in=8)

