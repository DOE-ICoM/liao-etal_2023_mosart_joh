
#create domain file

#create parameter file

#the flow direction will be the same as the coarse resolution case



#in practice, it is recommended to run hexwatershed using the following method, then call the post-processing

import os
import shutil
from pathlib import Path
from os.path import realpath

import cartopy.crs as ccrs

from pyearth.system.define_global_variables import *

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

from hexwatershed_utility.mosart.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf


from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.case.e3sm_create_case import e3sm_create_case
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file
from pye3sm.elm.general.structured.extract.elm_extract_data_mode_from_domain_file import elm_extract_data_mode_from_domain_file
from pye3sm.mesh.unstructured.e3sm_convert_unstructured_domain_file_to_scripgrid_file import e3sm_convert_unstructured_domain_file_to_scripgrid_file
from pye3sm.mesh.e3sm_create_structured_envelope_domain_file_1d import e3sm_create_structured_envelope_domain_file_1d
from pye3sm.mesh.e3sm_create_mapping_file import e3sm_create_mapping_file
from pye3sm.mesh.e3sm_map_domain_files import e3sm_map_domain_files

nTask = -5
iFlag_resubmit = 0
nSubmit = 0

iFlag_debug =0
iFlag_debug_case=0
iFlag_extract_forcing = 0

iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 0
iFlag_create_e3sm_case = 0

iFlag_mosart = 1 
iFlag_elm = 0 
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 1
iFlag_create_mapping_file = 0

sRegion = 'susquehanna'
sMesh_type = 'latlon'

iCase_index_hexwatershed = 1
sDate_hexwatershed='20230120'

iCase_index_e3sm = 2
sDate_e3sm='20230329'
dResolution_meter=5000

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
    sFilename = sWorkspace_output + '/' + sDate_hexwatershed  + 'submit.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

#post-process does not require job yet

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
                                                          iYear_data_datm_end_in = 2009, 
                                                          iYear_data_datm_start_in = 1980  , 
                                                          iCase_index_in = iCase_index_e3sm, 
                                                          sDate_in = sDate_e3sm, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,           
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )


oCase = pycase(aParameter_case)
sWorkspace_output = oCase.sWorkspace_case_aux

if not os.path.exists(sWorkspace_output):
    Path(sWorkspace_output).mkdir(parents=True, exist_ok=True)

#use the old domain as the domain reference file
sFilename_domain_ref = '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_domain.nc'
sFilename_parameter_ref = '/compyfs/liao313/04model/e3sm/susquehanna/cases_aux/e3sm20230329001/mosart_susquehanna_parameter.nc'

#mosart    
sFilename_mosart_parameter_out = sWorkspace_output + '/mosart_susquehanna_parameter.nc'
sFilename_mosart_structured_domain_out_1d= sWorkspace_output + '/mosart_susquehanna_domain.nc'
sFilename_mosart_structured_script_out = sWorkspace_output + '/mosart_susquehanna_scriptgrid.nc'

#elm
sFilename_elm_structured_domain_file_out_1d = sWorkspace_output + '/elm_susquehanna_domain.nc'
sFilename_elm_structured_script_out = sWorkspace_output + '/elm_susquehanna_scriptgrid.nc'



sFilename_map_elm_to_mosart = sWorkspace_output + '/l2r_susquehanna_mapping.nc'
sFilename_map_mosart_to_elm = sWorkspace_output + '/r2l_susquehanna_mapping.nc'

#copy reference file to the output folder
if not os.path.exists(sFilename_mosart_parameter_out):
    shutil.copyfile(sFilename_parameter_ref, sFilename_mosart_parameter_out)

if not os.path.exists(sFilename_mosart_structured_domain_out_1d):
    shutil.copyfile(sFilename_domain_ref, sFilename_mosart_structured_domain_out_1d)


#sFilename_user_dlnd_runoff_revised_05 = '/qfs/people/liao313/data/e3sm/dlnd.streams.txt.lnd.gpcc'
sFilename_user_dlnd_runoff_origin = '/qfs/people/liao313/data/e3sm/dlnd.streams.txt.lnd_005.gpcc' #the original 0.05 degree data
#we also need 1/8 and 1/16 degree data 
sFilename_user_dlnd_runoff = sWorkspace_output + '/dlnd.streams.txt.lnd.gpcc'

sFilename_domain_forcing = '/compyfs/liao313/00raw/mingpan_runoff/susquehanna/ming_daily_1980.nc'

#create the mapping file
dResolution_runoff = 0.05
if iFlag_create_mapping_file==1:
    #create two domain files
    
    #convert 2d structured domain file to 1d unstructured domain file
          
    #create a domain using mpas domain file        
    e3sm_create_structured_envelope_domain_file_1d(sFilename_mosart_structured_domain_out_1d, 
                                                   sFilename_elm_structured_domain_file_out_1d,
                                                                         dResolution_runoff, dResolution_runoff )
    # the second domain is for the model domain     
    
    sFilename_user_dlnd_runoff = '/compyfs/liao313/00raw/mingpan_runoff/susquehanna/dlnd.streams.txt.lnd_005.gpcc'
    #convert elm to script file         
    e3sm_convert_unstructured_domain_file_to_scripgrid_file(sFilename_elm_structured_domain_file_out_1d, sFilename_elm_structured_script_out )   
    
    #convert mosart to script file  
    e3sm_convert_unstructured_domain_file_to_scripgrid_file(sFilename_mosart_structured_domain_out_1d, sFilename_mosart_structured_script_out)

    e3sm_create_mapping_file( sFilename_elm_structured_script_out, sFilename_mosart_structured_script_out , sFilename_map_elm_to_mosart )

    e3sm_create_mapping_file( sFilename_mosart_structured_script_out , sFilename_elm_structured_script_out, sFilename_map_mosart_to_elm )

if iFlag_visualization_domain == 1:
    #visualize mosart input parameter generated∏
    #exclude flow direction maybe
    sFilename_domain_a = sFilename_mosart_structured_domain_out_1d
    sFilename_domain_b = sFilename_elm_structured_domain_file_out_1d
    aFilename_domain = [sFilename_domain_a, sFilename_domain_b]

    sFilename_out = sWorkspace_output + '/domain_comparison.png'
  
    e3sm_map_domain_files(aFilename_domain,sFilename_out)
    pass

if iFlag_create_e3sm_case == 1:
    #create the script file      
    aParameter_e3sm = pye3sm_read_e3sm_configuration_file(sFilename_e3sm_configuration ,
                                                          iFlag_debug_in = iFlag_debug, 
                                                          iFlag_branch_in = 0,
                                                          iFlag_continue_in = 0,
                                                          iFlag_resubmit_in = iFlag_resubmit,
                                                          iFlag_short_in = 0 ,
                                                          nSubmit_in= nSubmit,
                                                          nTask_in= nTask,
                                                          RES_in =res,
                                                          Project_in = project,
                                                          COMPSET_in = compset ,
                                                          sCIME_directory_in = sCIME_directory)
    oE3SM = pye3sm(aParameter_e3sm)
    if iFlag_mosart ==1:                
        sFilename_mosart_namelist = sWorkspace_output + slash + 'user_nl_rtm_' + oCase.sDate
        ofs = open(sFilename_mosart_namelist, 'w')        
     
        sLine = 'frivinp_rtm = ' + "'" + sFilename_mosart_parameter_out + "'" + '\n'
        ofs.write(sLine)

        sLine = "rtmhist_fincl1 = 'RIVER_DISCHARGE_OVER_LAND_LIQ', 'RIVER_DISCHARGE_TO_OCEAN_LIQ', 'Main_Channel_STORAGE_LIQ', 'Main_Channel_Water_Depth_LIQ','QSUR_LIQ','QSUR_ICE','QSUB_LIQ', 'QSUB_ICE'" + '\n'
        ofs.write(sLine)

        sLine = "rtmhist_fincl2 = 'RIVER_DISCHARGE_OVER_LAND_LIQ', 'Main_Channel_STORAGE_LIQ', 'Main_Channel_Water_Depth_LIQ' " + '\n'
        ofs.write(sLine)

        sLine = 'rtmhist_nhtfrq = 0,-24 '+ '\n'
        ofs.write(sLine)

        sLine = 'rtmhist_mfilt = 1,365 '+ '\n'
        ofs.write(sLine)
        
        #sLine = 'dlevelh2r = 20'+ '\n'
        #ofs.write(sLine)
        sLine = 'routingmethod = 1'+ '\n'
        #sLine = 'routingmethod = 2'+ '\n'
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
                                                          iFlag_debug_case_in= iFlag_debug_case,                                                   
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_replace_dlnd_forcing_in = 1,
                                                          iFlag_rof_in= 1,
                                                          iFlag_replace_drof_forcing_in = 1,
                                                          iYear_start_in = 1980, 
                                                          iYear_end_in = 2019,                                                          
                                                          iYear_data_datm_start_in = 1980, 
                                                          iYear_data_datm_end_in = 2009, 
                                                          iYear_data_dlnd_start_in = 1980, 
                                                          iYear_data_dlnd_end_in = 2019, 
                                                          iCase_index_in = iCase_index_e3sm, 
                                                          sDate_in = sDate_e3sm, 
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,
                                                          sFilename_atm_domain_in = sFilename_elm_structured_domain_file_out_1d,
                                                          sFilename_a2r_mapping_in = sFilename_map_elm_to_mosart,
                                                          sFilename_lnd_domain_in = sFilename_elm_structured_domain_file_out_1d,
                                                          sFilename_dlnd_namelist_in = sFilename_elm_namelist, 
                                                          sFilename_user_dlnd_runoff_in = sFilename_user_dlnd_runoff,
                                                          sFilename_l2r_mapping_in = sFilename_map_elm_to_mosart,
                                                          sFilename_rof_namelist_in = sFilename_mosart_namelist, 
                                                          sFilename_rof_parameter_in = sFilename_mosart_parameter_out, 
                                                          sFilename_r2l_mapping_in = sFilename_map_mosart_to_elm,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )
    pass
    #print(aParameter_case)

    oCase = pycase(aParameter_case)
    e3sm_create_case(oE3SM, oCase)

    
    pass


