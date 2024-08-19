import numpy as np
from hexwatershed_utility.mosart.find_gage_mesh_cell_id import find_gage_mesh_cell_id
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.toolbox.data.gsim.read_gsim_indices_data import read_gsim_indices_data
from pyearth.toolbox.date.day_in_month import day_in_month

#read text

sFilename_site = '/qfs/people/liao313/data/e3sm/amazon/mosart/GSIM_metadata/GSIM_catalog/GSIM_metadata.csv'

dummy  = text_reader_string(sFilename_site, iSkipline_in =1, cDelimiter_in=',', iFlag_remove_quota=1)

aLongitude_gage_in = np.array( dummy[:, 11]).astype(float)
aLatitude_gage_in = np.array( dummy[:, 10]).astype(float)
aDrainage_area_in = np.array([float(x) if x != 'NA' else np.nan for x in dummy[:, 13]]) * 1.0E6

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102007/mosart_amazon_parameter.nc'

aCellID_unstructured = find_gage_mesh_cell_id(aLongitude_gage_in, aLatitude_gage_in, aDrainage_area_in,
                            sFilename_domain_in,
                            sFilename_parameter_in,
                            dThreshold_difference_in = 0.15)

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240501004/mosart_amazon_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240501004/mosart_amazon_parameter.nc'

aCellID_structured = find_gage_mesh_cell_id(aLongitude_gage_in, aLatitude_gage_in, aDrainage_area_in,
                            sFilename_domain_in,
                            sFilename_parameter_in)

sFilename_site = '/compyfs/liao313/00raw/hydrology/gsim/GSIM_indices/TIMESERIES/monthly/ZW_0000081.mon'

iYear_start = 2010
iYear_end = 2019

aDate, aDischarge = read_gsim_indices_data(sFilename_site, iYear_start_in = iYear_start, iYear_end_in = iYear_end)



print(aDischarge)



