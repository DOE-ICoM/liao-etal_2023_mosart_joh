
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction



sFilename_domain_in= '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_parameter.geojson'
aVariable_parameter= ['nh','nt','rdep','rlen' ,'rslp', 'rwid','twid','tslp','twid','gxr','hslp']
aVariable_short= ['nh','nt','rdep','rlen' ,'rslp', 'rwid','twid','tslp','twid','gxr','hslp']
mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out, aVariable_parameter, aVariable_short)
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_flow_direction.geojson'
mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out)

