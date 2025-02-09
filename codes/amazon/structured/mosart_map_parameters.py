
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240501004/mosart_amazon_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240501004/mosart_amazon_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240501004/mosart_amazon_parameter.geojson'
aData_max_in = [None, None, None, None, None, None, None, None, None, None, None]

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

iFlag_parameter =1
iFlag_flow_direction =0
aLegend=list()
aLegend.append('(a)')
aLegend.append('Case 5')
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
                                             aLegend_in=aLegend,
                                            aExtent_in=aExtent)
if iFlag_flow_direction == 1:
    sFilename_geojson_out='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_flow_direction.geojson'
    dData_max = 6.0E6 #* 1.0E6
    dData_min = 0
    mosart_map_unstructured_flow_direction(sFilename_domain_in,
                                           sFilename_parameter_in,
                                             sFilename_geojson_out,
                                       iSize_x_in=8,
                                       iSize_y_in=8,
                                        dData_max_in = dData_max,
                                        dData_min_in = dData_min,
                                        aLegend_in=aLegend,
                                        aExtent_in=aExtent )

