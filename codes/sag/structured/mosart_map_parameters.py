
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_parameters import mosart_map_unstructured_parameters
from pye3sm.mosart.map.unstructured.mosart_map_unstructured_flow_direction import mosart_map_unstructured_flow_direction



sFilename_domain_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230101001/mosart_sag_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230101001/mosart_sag_parameter.nc'
sFilename_geojson_out='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230101001/mosart_sag_parameter.geojson'

aExtent = [-150.015625, -146.234375, 67.921875, 70.328125]

aVariable_parameter= ['nh','nt','rdep','rlen', 'rwid','rslp','twid','tslp','hslp','gxr']
aDate_max = [0.25, 0.25, 2.5, 10000, 300, 0.1, 50, 0.1, 0.1, 1E-3]

aVariable_parameter= ['rwid', 'rdep']
aVariable_short= ['rwid', 'rdep']
aTitle = ['Main channel width', 'Main channel depth']
aTitle = ['', '']
aDate_max = [0, 0]
aDate_max = [250, 2.50]
aUnit = ['Unit: m', 'Unit: m']

aFlag_scientific_notation_colorbar=[0 ,0]
aFlag_colorbar = [0,0]

iFlag_parameter =1
iFlag_flow_direction = 1
if iFlag_parameter == 1:
    mosart_map_unstructured_parameters(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                           aVariable_parameter,
                                           aVariable_short,
                                           aTitle,
                                           aFlag_colorbar_in = aFlag_colorbar,
                                           aFlag_scientific_notation_colorbar_in = aFlag_scientific_notation_colorbar,
                                           aData_max_in= aDate_max,
                                           aUnit_in= aUnit,
                                           iSize_x_in=6,
                                           iSize_y_in=8,
                                           aExtent_in=aExtent)



if iFlag_flow_direction == 1:
    sFilename_geojson_out='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20230101001/mosart_sag_flow_direction.geojson'
    mosart_map_unstructured_flow_direction(sFilename_domain_in, sFilename_parameter_in, sFilename_geojson_out,
                                       iSize_x_in=6, iSize_y_in=8, aExtent_in=aExtent)

