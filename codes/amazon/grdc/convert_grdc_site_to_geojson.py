#import pandas
import os
from osgeo import  osr #the default operator
from osgeo import gdal, ogr
import pandas as pd
#the grdc file in xlx format
sFilename_grdc_in = '/qfs/people/liao313/data/grdc/auxiliary/GRDC_Stations.xlsx'

#read the xlsx file using pandas
df = pd.read_excel(sFilename_grdc_in, sheet_name='station_catalogue', header=0)

#number of sites
nsite = df.shape[0]

#set geojson file name
sFilename_geosjon_out = '/qfs/people/liao313/data/grdc/auxiliary/GRDC_Stations.geojson'

#open geojson file for writing

pDriver_geojson = ogr.GetDriverByName('GeoJSON')     
pSpatial_reference_gcs = osr.SpatialReference()  
pSpatial_reference_gcs.ImportFromEPSG(4326)    # WGS84 lat/lon    

if os.path.exists(sFilename_geosjon_out):
    os.remove(sFilename_geosjon_out)


pDataset = pDriver_geojson.CreateDataSource(sFilename_geosjon_out)

#create a point layer
pLayer = pDataset.CreateLayer('site', pSpatial_reference_gcs, ogr.wkbPoint) 
# Add one attribute
pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution     
pLayer.CreateField(ogr.FieldDefn('name', ogr.OFTString)) #long type for high resolution  
pLayer.CreateField(ogr.FieldDefn('lon', ogr.OFTReal)) #long type for high resolution     
pLayer.CreateField(ogr.FieldDefn('lat', ogr.OFTReal)) #long type for high resolution         
pLayerDefn = pLayer.GetLayerDefn()
pFeature = ogr.Feature(pLayerDefn)      
#loop through all the ploygons
for i in range(0, nsite):
    #get the site id
    sSite_no = df.iloc[i]['grdc_no']
    #convert to string
    iSite_no = int(sSite_no)

    #get the lon from the dataframe
    dLongitude = df.iloc[i]['long']
    sLon = "{:0f}".format(dLongitude)
    dLatitude = df.iloc[i]['lat']
    sLat = "{:0f}".format(dLatitude)

    sName = df.iloc[i]['station']
    #create a point geometry
    pPoint = ogr.Geometry(ogr.wkbPoint)
    #assign the lon and lat
    pPoint.AddPoint(dLongitude, dLatitude)
   
    pFeature.SetGeometry(pPoint)
    
    pFeature.SetField( 'id', iSite_no )
    pFeature.SetField( 'lon', sLon )
    pFeature.SetField( 'lat', sLat )
    pFeature.SetField( 'name', sName )
    pLayer.CreateFeature(pFeature)          
pDataset = pLayer = pFeature = None # save, close


