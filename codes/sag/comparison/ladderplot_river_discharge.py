import sys
import numpy as np
from osgeo import ogr, osr, gdal
from datetime import datetime
import glob

import netCDF4 as nc
import matplotlib as mpl
from pyearth.system.define_global_variables import *

from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.gis.location.get_geometry_coordinates import get_geometry_coordinates
from pyearth.gis.geometry.calculate_distance_based_on_longitude_latitude import calculate_distance_based_on_longitude_latitude
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file


sPath_project = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh'
#add the project path of the pythonpath
sys.path.append(sPath_project)
from codes.shared.ladder_plot_xy_data import ladder_plot_xy_data
#use the site that is the furthest upstream

site_name  ='15905100'


#use this site to find the coordinates of the site
sFilename_site = '/qfs/people/liao313/data/e3sm/sag/mosart/gage_data_collection/gage_discharge_summary.csv'

dummy  = text_reader_string(sFilename_site, iSkipline_in =1, cDelimiter_in=',', iFlag_remove_quota=1)
aSitename = dummy[:, 0]
aLongitude_gage_in =  np.array( dummy[:, 3]).astype(float)
aLatitude_gage_in =  np.array( dummy[:, 2]).astype(float)
iSite_index = np.where(aSitename == site_name)[0][0]
dLongitude_site = aLongitude_gage_in[iSite_index]
dLatitude_site = aLatitude_gage_in[iSite_index]
#create a gdal point
pHeadwater = ogr.Geometry(ogr.wkbPoint)
pHeadwater.AddPoint(dLongitude_site, dLatitude_site)

#read the e3sm simulation using the cellid
sModel  = 'e3sm'
sRegion = 'sag'
sVariable = 'RIVER_DISCHARGE_OVER_LAND_LIQ'
sVariable1 = 'Main_Channel_Water_Depth_LIQ'
sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/e3sm.xml'
sFilename_case_configuration = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/data/sag/input/case.xml'
sWorkspace_scratch = '/compyfs/liao313'
iYear_start = 2019
iYear_end = 2019
iMonth_start = 1
iMonth_end = 12





#find which cell contains the site
sFilename_domain_geojson = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter_mesh.geojson'
pDriver = ogr.GetDriverByName('GeoJSON')
pDataset = pDriver.Open(sFilename_domain_geojson, gdal.GA_ReadOnly)
pLayer = pDataset.GetLayer(0)
pSrs = osr.SpatialReference()
pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
for pFeature in pLayer:
    pGeometry_in = pFeature.GetGeometryRef()
    sGeometry_type = pGeometry_in.GetGeometryName()
    dummyid= pFeature.GetField("id")
    if sGeometry_type =='POLYGON':
        if pHeadwater.Within(pGeometry_in):
            lHeadwaterID = dummyid
            break


#get the list of downstream cells
sFilename_parameter_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240101002/mosart_sag_parameter.nc'
pDomain = nc.Dataset(sFilename_parameter_in)
#read id and downstream id
for sKey in pDomain.variables.keys():
    if sKey == 'ID':
        aID = pDomain.variables[sKey][:]
    if sKey == 'dnID':
        aDownstreamID = pDomain.variables[sKey][:]
    if sKey == 'longxy':
        aLon = pDomain.variables[sKey][:]
    if sKey == 'latixy':
        aLat = pDomain.variables[sKey][:]

aCellID = list()
aCellIndex = list()
aCellLon = list()
aCellLat = list()

iIndex_start = np.where(aID == lHeadwaterID)[0][0]
aCellID.append(lHeadwaterID)
aCellIndex.append(iIndex_start)
aCellLon.append(aLon[iIndex_start])
aCellLat.append(aLat[iIndex_start])
lCellID_downslope = aDownstreamID[iIndex_start]
while lCellID_downslope !=-9999:
    aCellID.append(lCellID_downslope)
    index0 = np.where(aID ==lCellID_downslope )
    index= np.ravel(index0)[0]
    aCellIndex.append(index)
    lCellID_downslope = aDownstreamID[index]
    aCellLon.append(aLon[index])
    aCellLat.append(aLat[index])

#print(aCellID, aCellLon, aCellLat)

#calculate the distance reversely
aCellDistance_structured = np.full(len(aCellID), np.nan)
nCell = len(aCellID)
aCellDistance_structured[nCell-1] = 0.0
for i in range(nCell-2, -1, -1):
    dLongitude_from = aCellLon[i]
    dLatitude_from = aCellLat[i]
    dLongitude_to= aCellLon[i+1]
    dLatitude_to = aCellLat[i+1]
    distance = calculate_distance_based_on_longitude_latitude( dLongitude_from,
                                                   dLatitude_from,
                                                   dLongitude_to,
                                                   dLatitude_to)
    aCellDistance_structured[i] = aCellDistance_structured[i+1] + distance

print(aCellDistance_structured)

#read the e3sm simulation using the cellid

sDate_structured = '20240101'
iCase_index_e3sm_structurd = 2
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

#important, this is the cellid instead of the cell id


sWorkspace_case_aux = oCase_structured.sWorkspace_case_aux
sFilename_parameter = sWorkspace_case_aux + slash + '/mosart_'+ oCase_structured.sRegion + '_parameter.nc'
pDatasets_parameter = nc.Dataset(sFilename_parameter, 'r')
pDimension = pDatasets_parameter.dimensions.keys()


#aData_unstructured = np.full(nDay, np.nan, dtype= float)
aData_structured = np.full((nCell), np.nan, dtype= float)
#use the august in 2019 as an example

for iYear in range(iYear_start, iYear_end + 1):
    sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)
    for iMonth in range(8, 9, 1):
        sMonth = "{:02d}".format(iMonth)
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

                if sKey.lower() == sVariable1.lower() :
                    aData_variable1 = (aValue[:]).data
                    dFillvalue = float(aValue._FillValue )

            aData_structured = aData_variable[0, aCellIndex]
            aData_structured1 = aData_variable1[0, aCellIndex]


#find which cell contains the site
sFilename_domain_geojson = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter_mesh.geojson'
pDriver = ogr.GetDriverByName('GeoJSON')
pDataset = pDriver.Open(sFilename_domain_geojson, gdal.GA_ReadOnly)
pLayer = pDataset.GetLayer(0)
pSrs = osr.SpatialReference()
pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon
for pFeature in pLayer:
    pGeometry_in = pFeature.GetGeometryRef()
    sGeometry_type = pGeometry_in.GetGeometryName()
    dummyid= pFeature.GetField("id")
    if sGeometry_type =='POLYGON':
        if pHeadwater.Within(pGeometry_in):
            lHeadwaterID = dummyid
            break

#get the list of downstream cells
sFilename_parameter_in= '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_parameter.nc'
pDomain = nc.Dataset(sFilename_parameter_in)
#read id and downstream id
for sKey in pDomain.variables.keys():
    if sKey == 'ID':
        aID = pDomain.variables[sKey][:]
    if sKey == 'dnID':
        aDownstreamID = pDomain.variables[sKey][:]
    if sKey == 'longxy':
        aLon = pDomain.variables[sKey][:]
    if sKey == 'latixy':
        aLat = pDomain.variables[sKey][:]

aCellID = list()
aCellIndex = list()
aCellLon = list()
aCellLat = list()

iIndex_start = np.where(aID == lHeadwaterID)[0][0]
aCellID.append(lHeadwaterID)
aCellIndex.append(iIndex_start)
aCellLon.append(aLon[iIndex_start])
aCellLat.append(aLat[iIndex_start])
lCellID_downslope = aDownstreamID[iIndex_start]
while lCellID_downslope !=-9999:
    aCellID.append(lCellID_downslope)
    index0 = np.where(aID ==lCellID_downslope )
    index= np.ravel(index0)[0]
    aCellIndex.append(index)
    lCellID_downslope = aDownstreamID[index]
    aCellLon.append(aLon[index])
    aCellLat.append(aLat[index])

#print(aCellID, aCellLon, aCellLat)

#calculate the distance reversely
aCellDistance_unstructured = np.full(len(aCellID), np.nan)
nCell = len(aCellID)
aCellDistance_unstructured[nCell-1] = 0.0
for i in range(nCell-2, -1, -1):
    dLongitude_from = aCellLon[i]
    dLatitude_from = aCellLat[i]
    dLongitude_to= aCellLon[i+1]
    dLatitude_to = aCellLat[i+1]
    distance = calculate_distance_based_on_longitude_latitude( dLongitude_from,
                                                   dLatitude_from,
                                                   dLongitude_to,
                                                   dLatitude_to)
    aCellDistance_unstructured[i] = aCellDistance_unstructured[i+1] + distance

print(aCellDistance_unstructured)

sFilename_out = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/sag/ladder.geojson'
pDriver = ogr.GetDriverByName('GeoJSON')
pDataset = pDriver.CreateDataSource(sFilename_out)
pLayer = pDataset.CreateLayer('ladder', pSrs, ogr.wkbLinearRing)
pFeature = ogr.Feature(pLayer.GetLayerDefn())
pGeometry = ogr.Geometry(ogr.wkbLineString)
for i in range(nCell):
    pGeometry.AddPoint(aCellLon[i], aCellLat[i])
    pFeature.SetGeometry(pGeometry)
    pLayer.CreateFeature(pFeature)
pDataset = None

nyear = iYear_end - iYear_start + 1
nstress = 12 * nyear



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
#aData_unstructured = np.full((nCell), np.nan, dtype= float)
#use the august in 2019 as an example

for iYear in range(iYear_start, iYear_end + 1):
    sYear = "{:04d}".format(iYear) #str(iYear).zfill(4)
    for iMonth in range(8, 9, 1):
        sMonth = "{:02d}".format(iMonth)
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

                if sKey.lower() == sVariable1.lower() :
                    aData_variable1 = (aValue[:]).data
                    dFillvalue = float(aValue._FillValue )


            aData_unstructured = aData_variable[0, aCellIndex]
            aData_unstructured1 = aData_variable1[0, aCellIndex]

#read structured data




print('ready for plot')
aX_all = list()
aY_all = list()
aX_all.append(aCellDistance_structured)
aX_all.append(aCellDistance_unstructured)
aY_all.append(aData_structured)
aY_all.append(aData_unstructured)
aColor = ['red', 'blue']
aMarker= ['s', 'h']
aSize = np.full(2, mpl.rcParams['lines.markersize'])
aLinestyle = ['-', '--']
aLinewidth = [1.0,0.75]

aLabel_legend=['DRT mesh-based river discharge', 'MPAS mesh-based river discharge']

sFormat_x =  '%.1E'
sFormat_y =  '%.1E'
sLabel_x = 'Distance to outlet (m)'
sLabel_y = r'River discharge $(m^{3}/s)$'
sFilename_out = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/sag/ladderplot_river_discharge.png'

aY_all_twin_in= list()
aY_all_twin_in.append(aData_structured1)
aY_all_twin_in.append(aData_unstructured1)
ladder_plot_xy_data(aX_all,  aY_all,
        sFilename_out,
aY_all_twin_in=aY_all_twin_in, iFlag_twiny_in=1,aLabel_legend_twin_in=['DRT mesh-based water depth', 'MPAS mesh-based water depth'],dMax_y_twin_in=5.0,
        iDPI_in = None, aFlag_trend_in = None,
            iReverse_y_in = None,  iSize_x_in = None,
                    iFlag_scientific_notation_x_in=1,
                      iFlag_scientific_notation_y_in=1,
                iSize_y_in = None,  ncolumn_in = None,
                    dMax_x_in = 250000,  dMin_x_in = 0,
                    dMax_y_in =500, dMin_y_in = None,
                        dSpace_y_in = None,
                            aColor_in = aColor, aLinestyle_in = aLinestyle,  aLinewidth_in= aLinewidth, aMarker_in = aMarker,
                                aLabel_point_in = None,
                                    aTick_label_x_in = None,
                                    aLocation_legend_in = [1.0,1.0],
                                        sLabel_x_in = sLabel_x,
                                        sLabel_y_in = sLabel_y,
                                            aLabel_legend_in = aLabel_legend,
        sLocation_legend_in='upper right', sFormat_x_in = sFormat_x, sFormat_y_in =sFormat_y,
        sTitle_in = None)