#modify mingpan runoff so they can be used 

import os, sys
import numpy as np
import platform

import netCDF4 as nc

#import day_in_month from pyearth
from pyearth.system.define_global_variables import *
from pyearth.toolbox.date.day_in_month import day_in_month
sWorkspace_input = '/compyfs/liao313/00raw/mingpan_runoff/original'
sWorkspace_output = '/compyfs/liao313/00raw/mingpan_runoff/revised'
iYear_start = 1980
iYear_end = 2019

#set a conversion from mm/day to mm/s
conversion = 1.0/86400.0

def convert_mingpan_runoff(iYear_start, iYear_end):
    for iYear in range(iYear_start , iYear_end + 1, 1):

        sYear = '{:04d}'.format(iYear)

        sFilename = 'RUNOFF_' + sYear + '.nc'
        sFilename_out = 'ming_daily_' + sYear + '.nc'
        #open the netcdf file
        sFilename_in = os.path.join(sWorkspace_input, sFilename)
        sFilename_out = os.path.join(sWorkspace_output, sFilename_out)

        #read netcdf using nc.Dataset
        pDatasets_in = nc.Dataset(sFilename_in, 'r')
        netcdf_format = pDatasets_in.file_format
        pDatasets_out = nc.Dataset(sFilename_out, "w", format=netcdf_format) #'NETCDF3_CLASSIC')

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
                #unlimited_dim = pDatasets_out.createDimension(sKey, None)
    

        pDimension = pDatasets_in.dimensions.keys()
        for sKey, aValue in pDatasets_in.variables.items():    
            dummy = aValue.dimensions              

            if (sKey == 'ro'):             
                sKey = 'QOVER'       
                outVar = pDatasets_out.createVariable(sKey, aValue.datatype, dummy , zlib=True )        
                for sAttribute in aValue.ncattrs():            
                    outVar.setncatts( { sAttribute: aValue.getncattr(sAttribute) } )

                outVar[:] = aValue[:]  * conversion

                #add the last one
                sKey = 'QDRAI'       
                outVar = pDatasets_out.createVariable(sKey, aValue.datatype, dummy , zlib=True)        
                for sAttribute in aValue.ncattrs():            
                    outVar.setncatts( { sAttribute: aValue.getncattr(sAttribute) } )

                outVar[:] = 0.0 
                continue
            else:
                outVar = pDatasets_out.createVariable(sKey, aValue.datatype, dummy )        
                for sAttribute in aValue.ncattrs():            
                    outVar.setncatts( { sAttribute: aValue.getncattr(sAttribute) } )

                outVar[:] = aValue[:]  
                continue
            
        pDatasets_out.close()

if __name__ == "__main__":
    #retrive arguments
    #if len(sys.argv) == 3:
    #    iYear_start = int(sys.argv[1])
    #    iYear_end = int(sys.argv[2])
    convert_mingpan_runoff(iYear_start, iYear_end)

    

