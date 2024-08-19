
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction



sFilename_domain_in= '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_parameter.geojson'

aVariable_parameter= [ 'rwid','rdep','rlen' ,'rslp','twid','tslp','hslp','gxr','nh','nt']
aVariable_short= ['rwid','rdep','rlen' ,'rslp', 'twid','tslp','hslp','gxr','nh','nt']

aTitle = ['Main channel width', 'Main channel depth', 'Main channel Length', 'Main channel slope',
      'Tributary channel width', 'Tributary channel slope', 'Hillslope Slope', 'Drainage density','Manning roughness coefficient', 'Manning roughness coefficient',]
aFlag_scientific_notation_colorbar = [0,0,0,1,0,0,0,0,0,1,0]

aVariable_parameter= ['rwid', 'rdep']
aVariable_short= ['rwid', 'rdep']
aTitle = ['Main channel width', 'Main channel depth']
aTitle = ['', '']
aDate_max = [0, 0]
aDate_max = [7000, 40]
aUnit = ['Unit: m', 'Unit: m']

aFlag_scientific_notation_colorbar=[0 ,0]
aFlag_colorbar = [0,0]
aColormap = ['YlGnBu', 'Blues']
aExtent= [-80.96294746398925, -48.94024314880371, -21.183916664123537, 6.4270845413208]
iFlag_parameter =0
iFlag_flow_direction = 1

if iFlag_parameter == 1:
      mosart_map_unstructured_parameters(sFilename_domain_in,
                                          sFilename_parameter_in,
                                          sFilename_geojson_out,
                                         aVariable_parameter,
                                         aVariable_short,
                                         aTitle,
                                              aFlag_colorbar_in = aFlag_colorbar,
                                         aFlag_scientific_notation_colorbar_in = aFlag_scientific_notation_colorbar,
                                         aUnit_in=aUnit,
                                         aColormap_in=aColormap,
                                         aData_max_in=aDate_max,
                                            iSize_x_in=8,
                                            iSize_y_in=8,
                                              aExtent_in=aExtent)
if iFlag_flow_direction == 1:
      sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_flow_direction.geojson'
      mosart_map_unstructured_flow_direction(sFilename_domain_in,
                                             sFilename_parameter_in,
                                               sFilename_geojson_out,
                                       iSize_x_in=8,
                                       iSize_y_in=8,
                                       aExtent_in=aExtent)

