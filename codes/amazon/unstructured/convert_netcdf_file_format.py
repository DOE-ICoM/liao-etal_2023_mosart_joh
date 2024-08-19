import os
import numpy as np
import shutil
import netCDF4 as nc
def convert_netcdf_file_format(sFilename_old, sFilename_new):
    
    try:
        import netCDF4 as nc
    except ImportError as e:
        raise ImportError("The package 'netCDF4' is required for this function to run.") from e
    
    if os.path.exists(sFilename_old):
        print("Yep, I can read that file!")
    else:
        print("Nope, the path doesn't reach your file. Go research filepath in python")
        exit
    
    if os.path.exists(sFilename_new):
        os.remove(sFilename_new)


    pDatasets_in = nc.Dataset(sFilename_old)
    netcdf_format = pDatasets_in.file_format
    #output file
    pDatasets_out = nc.Dataset(sFilename_new, "w", format='NETCDF3_CLASSIC')
    aDimension_key=list()
    aDimension_value=list()
    for sKey, iValue in pDatasets_in.dimensions.items():
        dummy = len(iValue)
        if not iValue.isunlimited():            
            aDimension_key.append(sKey)
            aDimension_value.append(sKey)
            pDatasets_out.createDimension(sKey, dummy)            
        else:
            pDatasets_out.createDimension(sKey, dummy )

    #Copy variables
    for sKey, aValue in pDatasets_in.variables.items():        
        
        # we need to take care of rec dimension
        dummy = aValue.dimensions
        outVar = pDatasets_out.createVariable(sKey, aValue.datatype, dummy )        
        for sAttribute in aValue.ncattrs():            
            outVar.setncatts( { sAttribute: aValue.getncattr(sAttribute) } )

        outVar[:] = aValue[:]
        # close the output file
    #add new variable 


    
    pDatasets_out.close()



if __name__ == '__main__':
    
    sFilename_in = '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102005/mosart_amazon_parameter.nc'
    sFilename_out = '/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102005/mosart_amazon_parameter_new.nc'
    convert_netcdf_file_format(sFilename_in, sFilename_out)
    
    print('Done')