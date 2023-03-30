#in practice, it is recommended to run hexwatershed using the following method, then call the post-processing

import os

from pathlib import Path
from os.path import realpath

import cartopy.crs as ccrs

from pyearth.system.define_global_variables import *

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
from pyhexwatershed.classes.pycase import hexwatershedcase

from hexwatershed_utility.mosart.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf


from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.case.e3sm_create_case import e3sm_create_case
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file
from pye3sm.mesh.unstructured.e3sm_convert_unstructured_domain_file_to_scripgrid_file import e3sm_convert_unstructured_domain_file_to_scripgrid_file
from pye3sm.mesh.e3sm_create_structured_envelope_domain_file_1d import e3sm_create_structured_envelope_domain_file_1d
from pye3sm.mesh.e3sm_create_mapping_file import e3sm_create_mapping_file


iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_create_e3sm_case = 1

iFlag_mosart =1 
iFlag_elm =0 
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 0
iFlag_create_mapping_file = 1

sRegion = 'susquehanna'
sMesh_type = 'mpas'

iCase_index_hexwatershed = 1
iCase_index_e3sm = 7

dResolution_meter=5000
sDate='20230120'


res='MOS_USRDAT'      
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'

aExtent_full = [-150.1,-146.3, 67.8,70.7]
dLongitude_outlet_degree=-148.36105
dLatitude_outlet_degree=69.29553
pProjection_map = ccrs.Orthographic(central_longitude=  dLongitude_outlet_degree, \
        central_latitude= dLatitude_outlet_degree, globe=None)

sPath = str( Path().resolve() )

sPath = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/'
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  '/compyfs/liao313/04model/pyhexwatershed/susquehanna'
sCIME_directory ='/qfs/people/liao313/workspace/fortran/e3sm/E3SM/cime/scripts'



#generate a bash job script
if iFlag_create_hexwatershed_job ==1:
    sFilename = sWorkspace_output + '/' + sDate  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/susquehanna/pyhexwatershed_susquehanna_mpas_dam.json' )

    
if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()
    
#mpas mesh only has one resolution
iFlag_stream_burning_topology = 1 
iFlag_use_mesh_dem = 1
iFlag_elevation_profile = 1
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,
                iCase_index_in=iCase_index_hexwatershed, iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,
                iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,
                iFlag_elevation_profile_in=iFlag_elevation_profile,
                dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   

if iFlag_create_hexwatershed_job ==1:

    if iFlag_run_hexwatershed == 1:
        oPyhexwatershed._create_hpc_job()   
        sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)
        ofs.close()

        pass
else:
    pass


    
#post-process does not require job yet
sFilename_json_in='/compyfs/liao313/04model/pyhexwatershed/susquehanna/pyhexwatershed20220607001/hexwatershed/hexwatershed.json'

sFilename_mpas_in='/people/liao313/workspace/python/pyhexwatershed_icom/data/susquehanna/input/lnd_cull_mesh.nc'
sFilename_mosart_parameter_in = '/compyfs/inputdata/rof/mosart/MOSART_Global_half_20210616.nc'

#this one should be replace 
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,
                                                          iFlag_lnd_spinup_in = 0,
                                                          iFlag_atm_in = 0,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = 1980, 
                                                          iYear_end_in = 2019,
                                                          iYear_data_end_in = 2009, 
                                                          iYear_data_start_in = 1980  , 
                                                          iCase_index_in = iCase_index_e3sm, 
                                                          sDate_in = sDate, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,           
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )


oCase = pycase(aParameter_case)
sWorkspace_output = oCase.sWorkspace_case_aux

if not os.path.exists(sWorkspace_output):
    Path(sWorkspace_output).mkdir(parents=True, exist_ok=True)
 
    
sFilename_mosart_parameter_out = sWorkspace_output + '/mosart_susquehanna_parameter_mpas.nc'
sFilename_mosart_unstructured_domain= sWorkspace_output + '/mosart_susquehanna_domain_mpas.nc'
sFilename_mosart_unstructured_script = sWorkspace_output + '/mosart_susquehanna_scriptgrid_mpas.nc'

sFilename_elm_structured_domain_file_out_1d = sWorkspace_output + '/elm_susquehanna_domain_latlon.nc'
sFilename_elm_structured_script_1d = sWorkspace_output + '/elm_susquehanna_scripgrid_latlon.nc'

sFilename_map_elm_to_mosart = sWorkspace_output + '/l2r_susquehanna_mapping.nc'
sFilename_map_mosart_to_elm = sWorkspace_output + '/r2l_susquehanna_mapping.nc'

if iFlag_run_hexwatershed_utility == 1:
    #the json should replaced

    sFilename_json_in = oPyhexwatershed.sFilename_hexwatershed_json

    
    convert_hexwatershed_json_to_mosart_netcdf(sFilename_json_in, \
            sFilename_mpas_in, \
            sFilename_mosart_parameter_in,
            sFilename_mosart_parameter_out,\
            sFilename_mosart_unstructured_domain)

#create the mapping file
if iFlag_create_mapping_file==1:
    #create a domain using mpas domain file        
    e3sm_create_structured_envelope_domain_file_1d(sFilename_mosart_unstructured_domain, sFilename_elm_structured_domain_file_out_1d,
                                                                         0.5, 0.5 )
    #convert elm to script file         
    e3sm_convert_unstructured_domain_file_to_scripgrid_file(sFilename_elm_structured_domain_file_out_1d, sFilename_elm_structured_script_1d )   
    
    #convert mosart to script file  
    e3sm_convert_unstructured_domain_file_to_scripgrid_file(sFilename_mosart_unstructured_domain, sFilename_mosart_unstructured_script)

    e3sm_create_mapping_file( sFilename_elm_structured_script_1d, sFilename_mosart_unstructured_script , sFilename_map_elm_to_mosart )

    e3sm_create_mapping_file(  sFilename_mosart_unstructured_script , sFilename_elm_structured_script_1d, sFilename_map_mosart_to_elm )

if iFlag_visualization_domain == 1:
    #visualize mosart input parameter generated∏
    #exclude flow direction maybe
    pass

if iFlag_create_e3sm_case == 1:
    #create the script file      
    aParameter_e3sm = pye3sm_read_e3sm_configuration_file(sFilename_e3sm_configuration ,\
                                                          iFlag_debug_in = 0, \
                                                          iFlag_branch_in = 0,\
                                                          iFlag_continue_in = 0,\
                                                          iFlag_resubmit_in = 0,\
                                                          iFlag_short_in = 0 ,\
                                                          RES_in =res,\
                                                         Project_in = project,\
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

    if iFlag_elm == 0:   
        sFilename_elm_namelist = sWorkspace_output + slash + 'user_nl_elm_' + oCase.sDate
        ofs = open(sFilename_elm_namelist, 'w')
        #sLine = 'rtmhist_nhtfrq=0' + '\n'
        #ofs.write(sLine)
        sLine = 'dtlimit=2.0e0' + '\n'
        ofs.write(sLine)
        ofs.close()    
    aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,                                                        
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = 1980, 
                                                          iYear_end_in = 2019,
                                                          iYear_data_end_in = 1979, 
                                                          iYear_data_start_in = 1979  , 
                                                          iCase_index_in = iCase_index_e3sm, 
                                                          sDate_in = sDate, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,
                                                          sFilename_atm_domain_in = sFilename_elm_structured_domain_file_out_1d,
                                                          sFilename_a2r_mapping_in = sFilename_map_elm_to_mosart,
                                                          #sFilename_datm_namelist_in = sFilename_datm_namelist ,\
                                                          sFilename_lnd_domain_in = sFilename_elm_structured_domain_file_out_1d,
                                                          sFilename_dlnd_namelist_in = sFilename_elm_namelist, 
                                                          sFilename_l2r_mapping_in = sFilename_map_elm_to_mosart,
                                                          sFilename_rof_namelist_in = sFilename_mosart_namelist, 
                                                          sFilename_rof_parameter_in = sFilename_mosart_parameter_out, 
                                                          sFilename_r2l_mapping_in = sFilename_map_mosart_to_elm,

                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    pass
    #print(aParameter_case)

    oCase = pycase(aParameter_case)
    e3sm_create_case(oE3SM, oCase,     iFlag_replace_datm_forcing=0,    iFlag_replace_dlnd_forcing= 1)

    
    pass