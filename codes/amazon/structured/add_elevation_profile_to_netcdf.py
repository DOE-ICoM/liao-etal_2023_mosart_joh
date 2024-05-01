#this function is used to add the mpas elevation profile back to the mosart netcdf file

import os, sys
import numpy as np
import netCDF4 as nc
import shutil

sPath = '/qfs/people/liao313/workspace/python/subset/'
sys.path.append(sPath)

from subset.subset_raster import subset_raster

sFilename_raster_in = '/compyfs/liao313/00raw/dem/amazon/hyd_sa_dem_15s.tif'
sFilename_geojson_in = '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/domain.geojson' 


def add_variables_to_netcdf(sFilename_mosart, variable_names):
    #open the netcdf files
   
    f_mosart = nc.Dataset(sFilename_mosart, 'r')

    #first we will delete the variable by coping to a new netcdf file
    sFilename_mosart_temp = sFilename_mosart + '_temp'
    f_mosart_temp = nc.Dataset(sFilename_mosart_temp, 'w')
    #copy dimension as well
    for sKey, aValue in f_mosart.dimensions.items():
        f_mosart_temp.createDimension(sKey, len(aValue) if not aValue.isunlimited() else None)

    #copy global attributes
    for sKey in f_mosart.ncattrs():
        f_mosart_temp.setncattr(sKey, getattr(f_mosart, sKey))
    #copy variables
    for sKey, aValue in f_mosart.variables.items():        
        f_mosart_temp.createVariable(sKey, aValue.datatype, aValue.dimensions, fill_value=-9999)
        f_mosart_temp[sKey][:] = f_mosart[sKey][:]
        for attr in aValue.ncattrs():
            if attr not in ['_FillValue', 'missing_value']:
                f_mosart_temp[sKey].setncattr(attr, getattr(f_mosart[sKey], attr))
    
    f_mosart.close()
    f_mosart_temp.close()
    f_mosart = None
    #then we can saftly delelte the original netcdf file

    #shutil.move(sFilename_mosart_temp, sFilename_mosart)
    #reopen the new netcdf file
    f_mosart = nc.Dataset(sFilename_mosart_temp, 'a')
    
    #read the global id from the mosart netcdf file
    for sKey, aValue in f_mosart.variables.items():
        if sKey == 'ID':
            mosart_global_id0 = aValue
    
    aMosart_global_id = mosart_global_id0[:]
    nCell = len(aMosart_global_id)
    nElevation_profile = 11
    aElevation_profile_all = np.full((nCell, nElevation_profile), -9999.0, dtype=float)
    #calculate the elevation profile using dem    
    vData=subset_raster(sFilename_raster_in, sFilename_geojson_in) 
    
    
    for j in range(nCell):
        pData = vData[j]
        #create a 11 element numpy array to store the result 
        aElevation_profile = np.zeros(nElevation_profile)      
        #remove the missing value
        aData = pData[np.where(pData != -9999)]
        #call the numpy percentile function
        aElevation_profile[0] = np.min(aData)
        aElevation_profile[nElevation_profile-1] = np.max(aData)
        for i in range(1, nElevation_profile-1):
            aElevation_profile[i] = np.percentile(aData, i*10)    

        aElevation_profile_all[j,:] = aElevation_profile
    
    #loop over the variable names
    nVariable = len(variable_names)
    aElevation_flip = list()

    for i in range(nVariable):
        mosart_var = aElevation_profile_all[:,i]
        var_name = variable_names[i]
        if var_name in f_mosart.variables:
            # If the variable exists, update its data
            pvar = f_mosart.variables[var_name]
            pvar[:] = mosart_var
            #add attribute to the variable
            pvar.setncattr("units", "meters")            
            pvar.setncattr("long name", "") 
        else:
            # If the variable doesn't exist, create it and set its data
            pvar = f_mosart.createVariable(var_name, 'f8', ('gridcell'), fill_value=-9999)
            pvar[:] = mosart_var
            #add attribute to the variable
            pvar.setncattr("units", "meters")            
            pvar.setncattr("long name", "")    

        
        #flatten as 1d
        mosart_var=mosart_var.flatten()
        aElevation_flip.append(mosart_var)

    

    #create a merged one
    # If the variable doesn't exist, create it and set its data
    aElevation_flip = np.array(aElevation_flip)
    aElevation_flip=aElevation_flip.reshape(nVariable, nCell)
    pvar = f_mosart.createVariable('ele', 'f8', ('nele','gridcell'), fill_value=-9999)
    pvar[:] = aElevation_flip
    #add attribute to the variable
    pvar.setncattr("units", "meters")            
    pvar.setncattr("long name", "")    

         
 
    f_mosart.close()
    
    return

if __name__ == '__main__':
    variable_names = ['ele0', 'ele1','ele2','ele3','ele4','ele5','ele6','ele7','ele8','ele9','ele10']
    sFilename_mosart = '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20230501001/mosart_amazon_parameter.nc' 


    add_variables_to_netcdf(sFilename_mosart, variable_names)
    
    print('Done')