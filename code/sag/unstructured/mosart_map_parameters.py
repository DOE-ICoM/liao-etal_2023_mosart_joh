
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230401002/mosart_sag_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230401002/mosart_sag_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230401002/mosart_sag_parameter.geojson'
aDate_max = [0.25, 0.25, 2.5, 10000, 300, 0.1, 50, 0.1, 0.1, 1E-3]
aExtent = [-150.015625, -146.234375, 67.921875, 70.328125]
mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                   aData_max_in= aDate_max,
                                      iSize_x_in=6, iSize_y_in=8, aExtent_in=aExtent)
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230401002/mosart_sag_flow_direction.geojson'
mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                        iSize_x_in=6, iSize_y_in=8, aExtent_in=aExtent)

