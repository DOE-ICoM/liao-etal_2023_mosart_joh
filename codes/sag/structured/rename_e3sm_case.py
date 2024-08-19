from pye3sm.case.e3sm_rename_case import e3sm_rename_case
sModel = 'e3sm'
sRegion = 'sag'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/case.xml'
sDate = '20240101'

sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/Sag_16th_Ming_Runoff.2023-04-17-224706'

sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/Sag_16th_Ming_Runoff.2023-11-30-140738'

sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/Sag_16th_Ming_Runoff_Inund.2024-05-31-105615'

e3sm_rename_case(sFilename_case_configuration,
                 sDate,
                 sWorkspace_original_in,
                 iCase_index_in=2,
                 iYear_start_in=1980,
                 iYear_end_in=2019,
                 sModel_in=sModel,
                 sRegion_in=sRegion)
