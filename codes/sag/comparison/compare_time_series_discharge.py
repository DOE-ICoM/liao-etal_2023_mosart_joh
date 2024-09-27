import os
import numpy as np
import netCDF4 as nc #read netcdf
from datetime import datetime
from osgeo import ogr, osr
import glob
from pyearth.system.define_global_variables import *
from pyearth.visual.timeseries.plot_time_series_data import plot_time_series_data
from pyearth.visual.scatter.scatter_plot_data import scatter_plot_data
from pyearth.visual.scatter.scatter_plot_multiple_data import scatter_plot_multiple_data
from pyearth.toolbox.data.nwis.retrieve_nwis_discharge import retrieve_nwis_discharge

from pyearth.toolbox.data.convert_time_series_daily_to_monthly import convert_time_series_daily_to_monthly
from hexwatershed_utility.mosart.convert_hexwatershed_output_to_mosart import convert_hexwatershed_json_to_mosart_netcdf

from hexwatershed_utility.mosart.calculate_nse import calculate_nse
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.toolbox.date.day_in_month import day_in_month
from hexwatershed_utility.mosart.find_gage_mesh_cell_id import find_gage_mesh_cell_id
import pyearth.toolbox.date.julian as julian
current_file_path = os.path.abspath(__file__)
print(current_file_path)
current_file_directory = os.path.dirname(current_file_path)
print(current_file_directory)
iFlag_run_hexwatershed  = 0
iFlag_run_hexwatershed_utility = 1
iFlag_create_e3sm_case = 1

iFlag_mosart =1
iFlag_elm =0
iFlag_create_hexwatershed_job = 0
iFlag_visualization_domain = 0
iFlag_create_mapping_file = 1

sRegion = 'sag'
sMesh_type = 'mpas'

res='MOS_USRDAT'
res = 'MOS_USRDAT_MPAS'
compset = 'RMOSGPCC'
project = 'esmd'

iCase_index_hexwatershed = 1
iCase_index_e3sm = 1

dResolution_meter=5000
sDate='20230501'
#this one should be replace
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/case.xml'
sModel  = 'e3sm'
sWorkspace_scratch = '/compyfs/liao313'

#determine the max and min from modeled results
sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'

aDate= list()
iYear_start = 2000
iYear_end = 2019
iMonth_start = 1
iMonth_end = 12
nyear = iYear_end - iYear_start + 1
nstress = 12 * nyear

for iYear in range(iYear_start,iYear_end+1):
    for iMonth in range(1,13):
        #get day count in this month
        aDate.append(datetime(iYear,iMonth,15))

aDate = np.array(aDate)
nMonth = len(aDate)

aDate_daily= list()

for iYear in range(iYear_start, iYear_end+1):
    for iMonth in range(1,13):
        #get day count in this month
        iDay_end = day_in_month(iYear, iMonth)
        for iDay in range(1,iDay_end+1):
            aDate_daily.append(datetime(iYear,iMonth,iDay))

aDate_daily = np.array(aDate_daily)
nDay = len(aDate_daily)

sFilename_site = '/qfs/people/liao313/data/e3sm/sag/mosart/gage_data_collection/gage_discharge_summary.csv'

dummy  = text_reader_string(sFilename_site, iSkipline_in =1, cDelimiter_in=',', iFlag_remove_quota=1)
aSitename = dummy[:, 0]
#aRivername = dummy[:, 8]
aLongitude_gage_in =  np.array( dummy[:, 3]).astype(float)
aLatitude_gage_in =  np.array( dummy[:, 2]).astype(float)
aDrainage_area_in = np.array([float(x) if x != 'NA' else np.nan for x in dummy[:, 5]]) *1.0E-6
sFilename_domain_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_domain.nc'
#sFilename_parameter_structured_in='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter.nc'
sFilename_parameter_structured_in='/compyfs/icom/liao-etal_2023_mosart_joh/code/matlab/inputdata/MOSART_SAG_16th_with_ele_c240822.nc'

#copy it to the simulation folder

aIndex_structured, aCellID_structured, aDrainage_area_structured = find_gage_mesh_cell_id(aSitename, aLongitude_gage_in, aLatitude_gage_in, aDrainage_area_in,
                            sFilename_domain_in,
                            sFilename_parameter_structured_in,
                            dThreshold_drainage_in = 1.0E2,
                            dThreshold_difference_in = 0.10,
                            iFlag_data_km_in =0,
                            dBuffer_in = 0.1 )
#aIndex_structured is the index in the gage list
#aCellID_structured is the actual id in the mesh

sFilename_domain_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_domain.nc'
sFilename_parameter_unstructured_in='/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter.nc'
aIndex_unstructured, aCellID_unstructured, aDrainage_area_unstructured = find_gage_mesh_cell_id(aSitename, aLongitude_gage_in, aLatitude_gage_in, aDrainage_area_in,
                            sFilename_domain_in,
                            sFilename_parameter_unstructured_in,
                            dThreshold_drainage_in = 1.0E2,
                            dThreshold_difference_in = 0.10,
                            iFlag_data_km_in =0,
                            dBuffer_in = 0.1 )
#aIndex_unstructured is the index in the gage list


#find common cell id between structured and unstructured
aIndex_common,  cell_index_structured, cell_index_unstructured  = np.intersect1d(aIndex_structured, aIndex_unstructured, return_indices=True)
#cell_index_structured is the index in the structured mesh
#cell_index_unstructured is the index in the unstructured mesh

nCell_shared = len(aIndex_common)
#covnert cellid to cell index
#lCell_shared_structured = np.array(aIndex_structured)[cell_index_structured].astype(int)
lCell_index_structured = np.full(nCell_shared, -9999, dtype= int)
aDatasets = nc.Dataset(sFilename_parameter_structured_in)
for sKey, aValue in aDatasets.variables.items():
        # Copy variable attributes
        #outVar.setncatts({k: aValue.getncattr(k) for k in aValue.ncattrs()})
        if sKey == 'CellID':
            aCellID =  (aValue[:]).data
            iFlag_global_id = 1
        if sKey == 'ID':
            aID =  (aValue[:]).data
for i in range(nCell_shared):
    iindex =cell_index_structured[i]
    iCellID  = aCellID_structured[iindex]
    lCell_index_structured[i] = np.where(aID == iCellID)[0]
aDatasets = None
#lCell_shared_unstructured = np.array(aIndex_unstructured)[cell_index_unstructured].astype(int)
lCell_index_unstructured = np.full(nCell_shared, -9999, dtype= int)
aDatasets = nc.Dataset(sFilename_parameter_unstructured_in)
for sKey, aValue in aDatasets.variables.items():
        # Copy variable attributes
        #outVar.setncatts({k: aValue.getncattr(k) for k in aValue.ncattrs()})
        if sKey == 'CellID':
            aCellID =  (aValue[:]).data
            iFlag_global_id = 1
        if sKey == 'ID':
            aID =  (aValue[:]).data
for i in range(nCell_shared):
    iindex = cell_index_unstructured[i]
    iCellID  = aCellID_unstructured[iindex]
    lCell_index_unstructured[i] = np.where(aID == iCellID)[0]
aDatasets = None

aParameter_e3sm = pye3sm_read_e3sm_configuration_file(sFilename_e3sm_configuration ,\
                                                          iFlag_debug_in = 0, \
                                                          iFlag_branch_in = 0,\
                                                          iFlag_continue_in = 0,\
                                                          iFlag_resubmit_in = 0,\
                                                          iFlag_short_in = 0 ,\
                                                          RES_in =res,\
                                                         Project_in = project,\
                                                          COMPSET_in = compset)
oE3SM = pye3sm(aParameter_e3sm)

#read structure mosart result
sDate_structured = '20240101'
iCase_index_e3sm_structurd = 2

dData_min = 0
dData_max = -9999
aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = iYear_start,
                                                          iYear_end_in = iYear_end,
                                                          iCase_index_in = iCase_index_e3sm_structurd,
                                                          sDate_in = sDate_structured,
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )



oCase_structured = pycase(aParameter_case)
sWorkspace_analysis_case = sWorkspace_analysis_case = oCase_structured.sWorkspace_analysis_case
sWorkspace_simulation_case_run = oCase_structured.sWorkspace_simulation_case_run
sCase = oCase_structured.sCase
iMonth_start = 1
iMonth_end = 12
#id_structure  = 178
#aData_structured = np.full(nDay, np.nan, dtype= float)
aData_structured = np.full((nCell_shared,nstress ), np.nan, dtype= float)
#find out cell index
sWorkspace_case_aux = oCase_structured.sWorkspace_case_aux
sFilename_parameter = sWorkspace_case_aux + slash + '/mosart_'+ oCase_structured.sRegion + '_parameter.nc'
pDatasets_parameter = nc.Dataset(sFilename_parameter, 'r')
pDimension = pDatasets_parameter.dimensions.keys()

lIndex= 0
for iYear in range(iYear_start, iYear_end + 1):
    sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)
    for iMonth in range(1,13, 1):
        sMonth = "{:02d}".format(iMonth)
        iDay_end = day_in_month(iYear, iMonth)
        sDay = "{:02d}".format(iDay_end)
        sDate = sYear + '-'  + sMonth
        sPattern = '*.mosart.h0.' + sDate + "*" +sExtension_netcdf
        sFilepaths = sWorkspace_simulation_case_run + slash + sPattern
        aFilenames =  glob.glob(sFilepaths, recursive = False)
        iCount2 = len(aFilenames)
        if iCount2 == 1 :
            sFilename = aFilenames[0]
            #sFilename = sWorkspace_simulation_case_run + slash + sCase + sDummy
            pDatasets = nc.Dataset(sFilename)
            #get the variable
            for sKey, aValue in pDatasets.variables.items():
                if sKey.lower() == sVariable.lower():
                    aData_variable = (aValue[:]).data
                    #get fillvalue
                    dFillvalue = float(aValue._FillValue )
                    break

            aData_structured[:,lIndex ] = aData_variable[0,lCell_index_structured]
            lIndex = lIndex +1




sDate_unstructured = '20240103'
iCase_index_e3sm_unstructurd = 1
aParameter_case = pye3sm_read_case_configuration_file(sFilename_case_configuration,
                                                          iFlag_atm_in = 0,
                                                          iFlag_datm_in = 1,
                                                          iFlag_lnd_in= 0,
                                                          iFlag_dlnd_in= 1,
                                                          iFlag_rof_in= 1,
                                                          iYear_start_in = iYear_start,
                                                          iYear_end_in = iYear_end,
                                                          iCase_index_in = iCase_index_e3sm_unstructurd,
                                                          sDate_in = sDate_unstructured,
                                                          sModel_in = sModel,
                                                          sRegion_in = sRegion,
                                                          sVariable_in= sVariable,
                                                          sWorkspace_scratch_in =   sWorkspace_scratch )



oCase_unstructured = pycase(aParameter_case)
sWorkspace_analysis_case = sWorkspace_analysis_case = oCase_unstructured.sWorkspace_analysis_case
sWorkspace_simulation_case_run = oCase_unstructured.sWorkspace_simulation_case_run
sCase = oCase_unstructured.sCase

#important, this is the cellid instead of the cell id


sWorkspace_case_aux = oCase_unstructured.sWorkspace_case_aux
sFilename_parameter = sWorkspace_case_aux + slash + '/mosart_'+ oCase_unstructured.sRegion + '_parameter.nc'
pDatasets_parameter = nc.Dataset(sFilename_parameter, 'r')
pDimension = pDatasets_parameter.dimensions.keys()


#aData_unstructured = np.full(nDay, np.nan, dtype= float)
aData_unstructured = np.full((nCell_shared,nstress ), np.nan, dtype= float)
lIndex = 0
for iYear in range(iYear_start, iYear_end + 1):
    sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)
    for iMonth in range(1,13, 1):
        sMonth = "{:02d}".format(iMonth)
        iDay_end = day_in_month(iYear, iMonth)
        sDay = "{:02d}".format(iDay_end)
        sDate = sYear + '-'  + sMonth
        sPattern = '*.mosart.h0.' + sDate + "*" +sExtension_netcdf
        sFilepaths = sWorkspace_simulation_case_run + slash + sPattern
        aFilenames =  glob.glob(sFilepaths, recursive = False)
        iCount = len(aFilenames)
        if iCount ==1 :
            sFilename = aFilenames[0]
            pDatasets = nc.Dataset(sFilename)
            for sKey, aValue in pDatasets.variables.items():
                if sKey.lower() == sVariable.lower() :
                    aData_variable = (aValue[:]).data
                    dFillvalue = float(aValue._FillValue )
                    break

            aData_unstructured[:, lIndex] = aData_variable[0,lCell_index_unstructured]
            lIndex = lIndex + 1



sFolder_obs = '/qfs/people/liao313/data/e3sm/sag/mosart/gage_data_collection/'
sFolder_fig  ='/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/sag/gsim'

if not os.path.exists(sFolder_fig):
    os.makedirs(sFolder_fig)

aNSE_structured = np.full(nCell_shared, -9999, dtype= float)
aNSE_unstructured = np.full(nCell_shared, -9999, dtype= float)

dummy1 = datetime(iYear_start, 1, 1)
# dummy2 = datetime.datetime(iYear_end, iMonth_end, iDay_end)
lJulian_start = julian.to_jd(dummy1, fmt='jd')
#save log to a text file
sFilename_log = os.path.join(sFolder_fig, 'log.txt')
f = open(sFilename_log, 'w')
index_dry = np.arange(1, nstress, 12)
index_wet = np.arange(7, nstress, 12)
for iSite in range(nCell_shared):
    sSite = aSitename[aIndex_common[iSite]]

    sFolder_site = os.path.join(sFolder_obs, sSite)
    sFilename_site = os.path.join(sFolder_site, 'processed_daily_discharge_m3_s.csv')
    if not os.path.exists(sFilename_site):
        continue
    #read the obs
    dummy  = text_reader_string(sFilename_site, iSkipline_in =1, cDelimiter_in=',', iFlag_remove_quota=1)
    if dummy.shape[1] == 4:
        aDate_obs = dummy[:, 2]
        aDischarge_obs_daily = dummy[:, 3]
    else:
        aDate_obs = dummy[:, 0]
        aDischarge_obs_daily = dummy[:, 1]

    nObs = len(aDate_obs)
    aData_daily =np.full(nDay, np.nan, dtype= float)

    for iobs in range(nObs):
        sDate = aDate_obs[iobs]
        #get year, month, day
        iYear = int(sDate[0:4])
        iMonth = int(sDate[5:7])
        iDay = int(sDate[8:10])
        dummy2 = datetime(iYear, iMonth, iDay)
        lJulian = julian.to_jd(dummy2, fmt='jd')
        dummy_index = int(lJulian-lJulian_start)
        dummy3 = aDischarge_obs_daily[iobs]
        if dummy3 != 'NA' and dummy3 != '' and dummy_index >= 0 and dummy_index < nDay:
            aData_daily[dummy_index] = float(aDischarge_obs_daily[iobs])

    #convert daily data to monthly data
    aDischarge_obs = convert_time_series_daily_to_monthly(aData_daily,
                                         iYear_start,
                                         1,
                                         1,
                                         iYear_end,
                                         12,
                                         31,
                                         sType_in='mean')



    aDischarge_obs = np.array(aDischarge_obs)
    aData_structured0 =aData_structured[iSite]
    aData_unstructured0 =aData_unstructured[iSite]
    sFilename_out = os.path.join(sFolder_fig, sSite + '.png')

    #check if aDischarge_obs is all nan
    if np.isnan(aDischarge_obs).all():
        continue
    else:
        sLongitude = 'Longitude: ' + "{:.2f}".format(aLongitude_gage_in[aIndex_common[iSite]])
        sLatitude = 'Latitude: ' + "{:.2f}".format(aLatitude_gage_in[aIndex_common[iSite]])
        dDrainage_area = aDrainage_area_in[aIndex_common[iSite]]
        dDrainage_area_structured  = aDrainage_area_structured[cell_index_structured[iSite]]
        dDrainage_area_unstructured = aDrainage_area_unstructured[cell_index_unstructured[iSite]]
        sDrainage_area = 'drainage area: ' + "{:.2E}".format(dDrainage_area) + r' $km^{2}$'
        sDrainage_area_structured = 'drainage area: ' + "{:.2E}".format(dDrainage_area_structured)  + r' $km^{2}$'
        sDrainage_area_unstructured = 'drainage area: ' + "{:.2E}".format(dDrainage_area_unstructured)  + r' $km^{2}$'
        #only the first letter is capitalized
        #sName = sName.capitalize()
        sName = sSite
        sTitle = sName + ' (' + sLongitude + ', ' + sLatitude + ')'
        plot_time_series_data( [aDate, aDate, aDate], [aDischarge_obs, aData_structured0, aData_unstructured0],
                      sFilename_out = sFilename_out,
                      iFlag_scientific_notation_in = 1,
                      dMin_y_in = 0,
                      sTitle_in = sTitle,
                      sLabel_y_in= r'River discharge ($m^{3}/s$)',
                      aLabel_legend_in=['Observation, ' + sDrainage_area,'DRT mesh-based, ' + sDrainage_area_structured,'MPAS mesh-based, ' + sDrainage_area_unstructured],
                        aColor_in=['black','red','blue'],
                          aLinestyle_in=['solid','solid','solid'],
                            aMarker_in=['None','None','None'],
                             sLocation_legend_in = 'upper right')

        sFilename_out = os.path.join(sFolder_fig, sSite + '_scatter.png')
        dData_max = np.max([ np.nanmax(aData_structured0), np.nanmax(aData_unstructured0)])
        aData_x = list()
        aData_y = list()
        aData_x.append(aDischarge_obs)
        aData_x.append(aDischarge_obs)
        aData_y.append(aData_structured0)
        aData_y.append(aData_unstructured0)
        scatter_plot_data(aData_structured0,
                      aData_unstructured0,
                      sFilename_out,
                      iFlag_scientific_notation_x_in=1,
                      iFlag_scientific_notation_y_in=1,
                      iSize_x_in = None,
                      iSize_y_in = None,
                      iDPI_in = None ,
                      iFlag_log_x_in = None,
                      iFlag_log_y_in = None,
                      iFlag_lowess_in = None,
                      dMin_x_in = 0,
                      dMax_x_in = dData_max,
                      dMin_y_in = 0,
                      dMax_y_in = dData_max,
                      dSpace_x_in = None,
                      dSpace_y_in = None,
                      sFormat_x_in =None,
                      sFormat_y_in =None,
                      sLabel_x_in = 'DRT mesh-based river discharge ($m^{3}/s$)',
                      sLabel_y_in = 'MPAS mesh-based river discharge ($m^{3}/s$)' ,
                      sLabel_legend_in = None,
                      sTitle_in = None)

        #calculate difference
        diff = np.abs(aData_structured0 - aData_unstructured0)
        dummy = np.max([aData_structured0, aData_unstructured0], axis = 0)
        diff_ratio = diff/ dummy
        print(sName, np.max(diff_ratio), np.max(diff_ratio[index_dry]), np.max(diff_ratio[index_wet]))

        f.write(sName + ' ' + "{:.3f}".format(np.max(diff_ratio))
                 + ' ' + "{:.3f}".format(np.max(diff_ratio[index_dry]))
                 + ' ' + "{:.3f}".format(np.max(diff_ratio[index_wet]) ) + '\n')

        nse0 = calculate_nse(aDischarge_obs, aData_structured0)
        if nse0 < -1:
            nse0 = -1

        aNSE_structured[iSite] = nse0

        nse1 = calculate_nse(aDischarge_obs, aData_unstructured0)
        if nse1 < -1:
            nse1 = -1

        aNSE_unstructured[iSite] = nse1

#create a map of nse coefficient using point
sWorkspace_figure  = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/sag'
sFilename_geojson_nse = os.path.join(sWorkspace_figure, 'nse.geojson')


if os.path.exists(sFilename_geojson_nse):
    os.remove(sFilename_geojson_nse)



pDriver = ogr.GetDriverByName('GeoJSON')
pDataset_gage = pDriver.CreateDataSource(sFilename_geojson_nse)
pSpatial_reference_gcs = osr.SpatialReference()
pSpatial_reference_gcs.ImportFromEPSG(4326)    # WGS84 lat/long
pLayer_gage = pDataset_gage.CreateLayer('nse', pSpatial_reference_gcs, ogr.wkbPoint)
pLayer_gage.CreateField(ogr.FieldDefn('name', ogr.OFTString))
pLayer_gage.CreateField(ogr.FieldDefn('lon', ogr.OFTReal))
pLayer_gage.CreateField(ogr.FieldDefn('lat', ogr.OFTReal))
pLayer_gage.CreateField(ogr.FieldDefn('drai', ogr.OFTReal))
pLayer_gage.CreateField(ogr.FieldDefn('nse0', ogr.OFTReal))
pLayer_gage.CreateField(ogr.FieldDefn('nse1', ogr.OFTReal))

pLayerDefn = pLayer_gage.GetLayerDefn()

for iSite in range(nCell_shared):
    if aNSE_structured[iSite] != -9999 and aNSE_unstructured[iSite] != -9999:
        sSite = aSitename[aIndex_common[iSite]]
        pFeature = ogr.Feature(pLayerDefn)
        pFeature.SetField('name', sSite)
        pFeature.SetField('lon', aLongitude_gage_in[aIndex_common[iSite]])
        pFeature.SetField('lat', aLatitude_gage_in[aIndex_common[iSite]])
        pFeature.SetField('drai', aDrainage_area_in[aIndex_common[iSite]])
        pFeature.SetField('nse0', aNSE_structured[iSite])
        pFeature.SetField('nse1', aNSE_unstructured[iSite])
        pPoint = ogr.Geometry(ogr.wkbPoint)
        pPoint.AddPoint(aLongitude_gage_in[aIndex_common[iSite]], aLatitude_gage_in[aIndex_common[iSite]])
        pFeature.SetGeometry(pPoint)
        pLayer_gage.CreateFeature(pFeature)
    else:
        print('bad data')

f.close()
print('Finished')


