from pye3sm.case.e3sm_rename_case import e3sm_rename_case
sModel = 'e3sm'
sRegion ='susquehanna'

sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/susquehanna/case.xml'
sDate='20230329'


sWorkspace_original_in= '/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/outputs/Susquehanna_16th_Ming_Runoff.2023-02-15-123154/'
    


e3sm_rename_case(sFilename_case_configuration , sDate, sWorkspace_original_in, iCase_index_in = 1, \
        sModel_in = sModel, sRegion_in = sRegion)
    