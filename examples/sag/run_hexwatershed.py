#in practice, it is recommended to run hexwatershed using the following method, then call the post-processing

import os, sys, stat

from pathlib import Path
from os.path import realpath

import cartopy.crs as ccrs

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyearth.system.define_global_variables import *
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from hexwatershed_utility.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf
from pye3sm.case.e3sm_create_case import e3sm_create_case
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file

iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_mosart =1 
iFlag_create_job = 0
iFlag_visualization = 1

sRegion = 'sag'
sMesh_type = 'mpas'
iCase_index = 1
dResolution_meter=5000
sDate='20230120'


res='MOS_USRDAT'      
compset = 'RMOSGPCC'

aExtent_full = [-150.1,-146.3, 67.8,70.7]
dLongitude_outlet_degree=-148.36105
dLatitude_outlet_degree=69.29553
pProjection_map = ccrs.Orthographic(central_longitude=  dLongitude_outlet_degree, \
        central_latitude= dLatitude_outlet_degree, globe=None)

sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/sag' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/sag'
sCIME_directory ='/qfs/people/liao313/workspace/fortran/e3sm/E3SM/cime/scripts'



#generate a bash job script
if iFlag_create_job ==1:
    sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/sag/pyhexwatershed_sag_mpas.json' )

    
if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()
    
#mpas mesh only has one resolution
iFlag_stream_burning_topology = 1 
iFlag_use_mesh_dem = 1
iFlag_elevation_profile = 1
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
                iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                iFlag_elevation_profile_in=iFlag_elevation_profile,\
                dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
if iFlag_create_job ==1:

    if iFlag_run_hexwatershed == 1:
        oPyhexwatershed._create_hpc_job()
        print(iCase_index)
        sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)


        pass
else:
    pass


    
#post-process does not require job yet


if iFlag_run_hexwatershed_utility == 1:
    #the json should replaced
    sFilename_json_in='/compyfs/liao313/04model/pyhexwatershed/sag/pyhexwatershed20220607001/hexwatershed/hexwatershed.json'
    sFilename_mpas_in='/people/liao313/workspace/python/pyhexwatershed_icom/data/sag/input/lnd_mesh.nc'

    sFilename_mosart_parameter_in = '/compyfs/inputdata/rof/mosart/MOSART_Global_half_20210616.nc'

    #this one should be replace 
    sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/pye3sm/pye3sm/e3sm.xml'
    sFilename_case_configuration = '/qfs/people/liao313/workspace/python/pye3sm/pye3sm/case.xml'
    sModel  = 'e3sm'
    sWorkspace_scratch = '/compyfs/liao313'
    aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,\
                                                          iFlag_elm_spinup_in = 0,\
                                                          iFlag_atm_in = 0,\
                                                          iFlag_elm_in= 0,\
                                                          iFlag_mosart_in= 1,\
                                                          iYear_start_in = 2009, 
                                                          iYear_end_in = 2009,\
                                                          iYear_data_end_in = 2009, \
                                                          iYear_data_start_in = 1980  , \
                                                          iCase_index_in = iCase_index, \
                                                          sDate_in = sDate, \
                                                          sModel_in = sModel,\
                                                          sRegion_in = sRegion,           
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    pass
    #print(aParameter_case)

    oCase = pycase(aParameter_case)
    sWorkspace_output = oCase.sWorkspace_case_aux

    
    if not os.path.exists(sWorkspace_output):
        Path(sWorkspace_output).mkdir(parents=True, exist_ok=True)
 
    
    sFilename_mosart_parameter_out = sWorkspace_output + '/mosart_sag_parameter.nc'
    sFilename_mosart_domain_out = sWorkspace_output + '/mosart_sag_domain.nc'


    convert_hexwatershed_json_to_mosart_netcdf(sFilename_json_in, \
        sFilename_mpas_in, \
            sFilename_mosart_parameter_in,
            sFilename_mosart_parameter_out,\
            sFilename_mosart_domain_out)

    if iFlag_visualization ==1:
        #visualize mosart input parameter generated
        #exclude flow direction maybe
        pass
    aParameter_e3sm = pye3sm_read_e3sm_configuration_file(sFilename_e3sm_configuration ,\
                                                          iFlag_debug_in = 0, \
                                                          iFlag_branch_in = 0,\
                                                          iFlag_continue_in = 0,\
                                                          iFlag_resubmit_in = 0,\
                                                          iFlag_short_in = 1 ,\
                                                          RES_in =res,\
                                                          COMPSET_in = compset ,\
                                                          sCIME_directory_in = sCIME_directory)
    oE3SM = pye3sm(aParameter_e3sm)

    if iFlag_mosart ==1:        
        
        sFilename_mosart_namelist = sWorkspace_output + slash + 'user_nl_rtm_' + oCase.sDate
        ofs = open(sFilename_mosart_namelist, 'w')
        #sLine = 'rtmhist_nhtfrq=0' + '\n'
        #ofs.write(sLine)
        sLine = 'frivinp_rtm = ' + "'" + sFilename_mosart_parameter_out + "'" + '\n'
        ofs.write(sLine)
        #sLine = 'rtmhist_fincl1= "area"' + '\n'
        #ofs.write(sLine)
        sLine = 'routingmethod = 1'+ '\n'
        ofs.write(sLine)
        sLine = 'inundflag = .false.'+ '\n'
        ofs.write(sLine)
        #opt_elevprof = 1
        ofs.close()
    aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,\
                                                        
                                                          iFlag_atm_in = 0,\
                                                          iFlag_elm_in= 0,\
                                                          iFlag_mosart_in= 1,\
                                                          iYear_start_in = 2000, 
                                                          iYear_end_in = 2009,\
                                                          iYear_data_end_in = 2009, \
                                                          iYear_data_start_in = 1980  , \
                                                          iCase_index_in = iCase_index, \
                                                          sDate_in = sDate, \
                                                          sModel_in = sModel,\
                                                          sRegion_in = sRegion,\
                                                          
                                                          sFilename_mosart_namelist_in = sFilename_mosart_namelist, \
                                                          sFilename_mosart_parameter_in = sFilename_mosart_parameter_out, \
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    pass
    #print(aParameter_case)

    oCase = pycase(aParameter_case)
    e3sm_create_case(oE3SM, oCase,     iFlag_replace_datm_forcing=0,    iFlag_replace_dlnd_forcing= 0)

    
    pass