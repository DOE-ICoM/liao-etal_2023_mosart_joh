import numpy as np
from hexwatershed_utility.mosart.find_gage_mesh_cell_id import find_gage_mesh_cell_id


aLongitude_gage_in = [	-148.626,	-148.82323,	-148.85997,	-148.6714]
aLatitude_gage_in = [69.5958,69.15065,68.95835,69.9461]
aDrainage_area_in = np.array([11790,5800,4725,13500]) * 1.0E6

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_domain.nc'
sFilename_parameter_in='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter.nc'

find_gage_mesh_cell_id(aLongitude_gage_in, aLatitude_gage_in, aDrainage_area_in,
                            sFilename_domain_in,
                            sFilename_parameter_in)