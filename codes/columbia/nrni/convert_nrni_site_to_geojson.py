#import pandas
import os
from osgeo import  osr #the default operator
from osgeo import  ogr

#site information are obtained from here
#https://www.hydro.washington.edu/CRCC/data/
#number of sites and we will just copy paste the location becase the original format excel file is hard to work with
nsite = 2

aName=['BON','IHR']
aLon=[-121.9544444, -118.8819444]
aLat=[45.63333333, 46.25055556]

#set geojson file name
sFilename_geosjon_out = '/qfs/people/liao313/data/e3sm/columbia/mosart/BPA_NRNI_flow/NRNI_Stations.geojson'

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
  
pLayer.CreateField(ogr.FieldDefn('name', ogr.OFTString)) #long type for high resolution  
pLayer.CreateField(ogr.FieldDefn('lon', ogr.OFTReal)) #long type for high resolution     
pLayer.CreateField(ogr.FieldDefn('lat', ogr.OFTReal)) #long type for high resolution         
pLayerDefn = pLayer.GetLayerDefn()
pFeature = ogr.Feature(pLayerDefn)      
#loop through all the ploygons
for i in range(0, nsite):
    #get the site id
    sName = aName[i]
    

    #get the lon from the dataframe
    dLongitude = aLon[i]
    sLon = "{:0f}".format(dLongitude)
    dLatitude = aLat[i]
    sLat = "{:0f}".format(dLatitude)

  
    #create a point geometry
    pPoint = ogr.Geometry(ogr.wkbPoint)
    #assign the lon and lat
    pPoint.AddPoint(dLongitude, dLatitude)   
    pFeature.SetGeometry(pPoint)
    pFeature.SetField( 'name', sName )    
    pFeature.SetField( 'lon', sLon )
    pFeature.SetField( 'lat', sLat )
    
    pLayer.CreateFeature(pFeature)          
pDataset = pLayer = pFeature = None # save, close


