import os
from osgeo import ogr
from pyearth.toolbox.data.nwis.retrieve_usgs_site_information_nwis import retrieve_usgs_site_information_nwis

# USGS gage number for the stream of interest
aGage_num = ['15908000','15906000' ]  #'15896000' is not within the boundary

#create the time series 
# URL for the water data service API
current_file_path = os.path.abspath(__file__)
print(current_file_path)
current_file_directory = os.path.dirname(current_file_path)
print(current_file_directory)



#loop through all the gages
driver = ogr.GetDriverByName('GeoJSON')
output_file = current_file_directory + '/' 'site_location.geojson'
# Open the GeoJSON data source
if os.path.exists(output_file):
    os.remove(output_file)

data_source = driver.CreateDataSource(output_file)
pLayer = data_source.CreateLayer('points', geom_type=ogr.wkbPoint)

pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64))
pLayer.CreateField(ogr.FieldDefn('lon', ogr.OFTReal))
pLayer.CreateField(ogr.FieldDefn('lat', ogr.OFTReal))
pLayer.CreateField(ogr.FieldDefn('drainage', ogr.OFTReal))
pFeature = ogr.Feature(pLayer.GetLayerDefn())

for gage_num in aGage_num:
    dLon, dLat, dDrainage = retrieve_usgs_site_information_nwis(gage_num)
    print(dLon, dLat, dDrainage)      
   
  
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(dLon, dLat)
    pFeature.SetField('id', int(gage_num) ) 
    pFeature.SetField('lon', dLon ) 
    pFeature.SetField('lat', dLat ) 
    pFeature.SetField('drainage', dDrainage ) 
    pFeature.SetGeometry(point)
    pLayer.CreateFeature(pFeature)
    
data_source.Destroy()









