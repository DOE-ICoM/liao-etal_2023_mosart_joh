
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
mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out, aVariable_parameter, aVariable_short,
                                    aFlag_scientific_notation_colorbar_in= aFlag_scientific_notation_colorbar,
                                      iSize_x_in=7, iSize_y_in=8)
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_flow_direction.geojson'
mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                       iSize_x_in=7, iSize_y_in=8)

