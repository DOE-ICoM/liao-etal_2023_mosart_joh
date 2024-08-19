from pye3sm.case.e3sm_rename_case import e3sm_rename_case
sModel = 'e3sm'
sRegion ='amazon'
sFilename_case_configuration  = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/amazon/input/case.xml'
sDate='20240501'

sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/AMZ_8th_Ming_Runoff.2023-04-25-225438'

sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/AMZ_8th_Ming_Runoff_inund.2024-04-26-194001/'

sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/AMZ_8th_Ming_Runoff_inund.2024-05-31-140806'


sWorkspace_original_in = '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/AMZ_8th_Ming_Runoff_inund.2024-06-20-102226'

e3sm_rename_case(sFilename_case_configuration ,
                 sDate,
                 sWorkspace_original_in,
                 iCase_index_in = 4,
        sModel_in = sModel,
        sRegion_in = sRegion,
        iYear_start_in = 2000,
        iYear_end_in = 2019)
