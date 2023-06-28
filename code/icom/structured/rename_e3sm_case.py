from pye3sm.case.e3sm_rename_case import e3sm_rename_case
sModel = 'e3sm'
sRegion ='icom'
sFilename_case_configuration  = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/examples/icom/case.xml'
sDate='20230602'

sWorkspace_original_in= '/compyfs/tanz151/e3sm_scratch/ICoM_sed_USRDAT_I20TRGSWCNPRDCTCBC/'
    


e3sm_rename_case(sFilename_case_configuration , sDate, sWorkspace_original_in, iCase_index_in = 1, \
        sModel_in = sModel, sRegion_in = sRegion)
    