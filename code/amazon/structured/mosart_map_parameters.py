
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction



sFilename_domain_in= '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_parameter.geojson'


aData_max_in = [None, None, None, None, None, None, None, None, None, None, None]
mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out, aData_max_in= aDate_max,
                                      iSize_x_in=8, iSize_y_in=8)
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_flow_direction.geojson'
mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                       iSize_x_in=8, iSize_y_in=8)

