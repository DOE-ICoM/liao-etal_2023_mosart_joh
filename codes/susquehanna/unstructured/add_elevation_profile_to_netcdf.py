#this function is used to add the mpas elevation profile back to the mosart netcdf file


import numpy as np
import netCDF4 as nc
import shutil

def add_variables_to_netcdf(sFilename_mosart, sFilename_mpas, variable_names):
    #open the netcdf files
    f_mpas = nc.Dataset(sFilename_mpas, 'r')
    f_mosart = nc.Dataset(sFilename_mosart, 'a')

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
        if sKey not in variable_names:
            f_mosart_temp.createVariable(sKey, aValue.datatype, aValue.dimensions, fill_value=-9999)
            f_mosart_temp[sKey][:] = f_mosart[sKey][:]
            for attr in aValue.ncattrs():
                if attr not in ['_FillValue', 'missing_value']:
                    f_mosart_temp[sKey].setncattr(attr, getattr(f_mosart[sKey], attr))
    
    f_mosart.close()
    f_mosart_temp.close()
    f_mosart = None
    #then we can saftly delelte the original netcdf file

    shutil.move(sFilename_mosart_temp, sFilename_mosart)
    #reopen the new netcdf file
    f_mosart = nc.Dataset(sFilename_mosart, 'a')
    
    #read the global id from the mosart netcdf file
    for sKey, aValue in f_mosart.variables.items():
        if sKey == 'CellID':
            mosart_global_id0 = aValue
    
    aMosart_global_id = mosart_global_id0[:]
    

    #get the elevation profile from mpas
    for sKey, aValue in f_mpas.variables.items():    
        if sKey == 'indexToCellID':
            cellsOnCell0 = aValue 
        
        if sKey == 'bed_elevation_profile':
            bed_elevation_profile0 = aValue 
          
    aIndexToCellID = cellsOnCell0[:]
    aBed_elevation_profile = bed_elevation_profile0[:] 
    #create a dictionary with global_id as key and variable as value
    mpas_dict = dict(zip(aIndexToCellID, aBed_elevation_profile))
    #loop over the variable names
    nVariable = len(variable_names)
    aMosart_var = np.array([mpas_dict[id] for id in aIndexToCellID if id in aMosart_global_id])
    for i in range(nVariable):
        var_name = variable_names[i]
        #read the variable from the mpas netcdf file     
        mosart_var = aMosart_var[:,i]      
        if var_name in f_mosart.variables:
            # If the variable exists, update its data
            pvar = f_mosart.variables[var_name]
            pvar[:] = mosart_var
            #add attribute to the variable
            pvar.setncattr("units", "meters")            
            pvar.setncattr("long name", "") 
        else:
            # If the variable doesn't exist, create it and set its data
            pvar = f_mosart.createVariable(var_name, 'f8', ('gridcell',), fill_value=-9999)
            pvar[:] = mosart_var
            #add attribute to the variable
            pvar.setncattr("units", "meters")            
            pvar.setncattr("long name", "")       
       
    
    #close the netcdf files
    f_mpas.close()
    f_mosart.close()
    
    return

if __name__ == '__main__':
    variable_names = ['elev0', 'elev1','elev2','elev3','elev4','elev5','elev6','elev7','elev8','elev9','elev10']
    sFilename_mosart = '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20240102001/mosart_susquehanna_parameter.nc'
    sFilename_mpas = '/qfs/people/liao313/workspace/python/pyhexwatershed_icom/data/susquehanna/input/lnd_cull_mesh.nc'
    add_variables_to_netcdf(sFilename_mosart, sFilename_mpas, variable_names)
    
    print('Done')