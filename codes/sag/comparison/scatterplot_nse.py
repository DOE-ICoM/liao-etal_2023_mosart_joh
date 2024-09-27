import os, sys, stat
from pathlib import Path
from os.path import realpath
import json
import numpy as np
from osgeo import  osr, gdal, ogr
import matplotlib as mpl
from pyearth.system.define_global_variables import *
from pyearth.visual.scatter.scatter_plot_data import scatter_plot_data
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.toolbox.math.stat.remap import remap
sPath_project = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh'
sys.path.append(sPath_project)
from codes.shared.scatter_plot_multiple_data import scatter_plot_multiple_data


#read the geojson file
pDriver = ogr.GetDriverByName('GeoJSON')

aData_x=list()
aData_y=list()
aDrainage = list()
aRegion = list()
aRegion.append('sag')
aRegion.append('susquehanna')
aRegion.append('amazon')

#make the first letter capital
aLabel_legend = [x.capitalize() for x in aRegion]


sWorkspace_figure  = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/'
aDrainage_min = 1.0E8
aDrainage_max = -1.0E8
for i in range(3):
    sRegion = aRegion[i]
    sFilename_geojson_nse = os.path.join(sWorkspace_figure, sRegion , 'nse.geojson')
    pDataset = pDriver.Open(sFilename_geojson_nse, 0)
    pLayer = pDataset.GetLayer()
    nFeature = pLayer.GetFeatureCount()
    anse0 =list()
    anse1 =list()
    aDrainage1 = list()
    for i in range(nFeature):
        pFeature = pLayer.GetFeature(i)
        nse0 = pFeature.GetField('nse0')
        nse1 = pFeature.GetField('nse1')
        drainage = pFeature.GetField('drai')
        anse0.append(nse0)
        anse1.append(nse1)
        aDrainage1.append(drainage)


    aData_x.append(anse0)
    aData_y.append(anse1)
    aDrainage1 = np.array(aDrainage1)
    print(np.min(aDrainage1))
    print(np.max(aDrainage1))
    aDrainage_min = np.min([np.min(aDrainage1), aDrainage_min])
    aDrainage_max = np.max([np.max(aDrainage1), aDrainage_max])

    aDrainage.append(aDrainage1)

print(aDrainage_min, aDrainage_max)


#get min and max of drainage
iSize_min = 50
iSize_max = 200

aSize = list()
def remap_log_scale(values, min_val, max_val, new_min, new_max):
    # Apply logarithmic transformation
    log_values = np.log(values)
    log_min_val = np.log(min_val)
    log_max_val = np.log(max_val)

    # Remap the log-transformed values
    remapped_values = new_min + (log_values - log_min_val) * (new_max - new_min) / (log_max_val - log_min_val)
    return remapped_values

for i in range(3):
    aSize1 = list()
    aDrainage1 = aDrainage[i]
    for j in range(len(aDrainage1)):
        aDrainage2 = aDrainage1[j]
        iSize = remap_log_scale( aDrainage2, aDrainage_min, aDrainage_max, iSize_min, iSize_max )
        aSize1.append(iSize)

    aSize.append(aSize1)



sFilename_out = os.path.join(sWorkspace_figure, 'scatterplot_nse.png')
aColor = ['red', 'blue', 'green']
aMarker = ['o', '^', 's']
#aSize = [100, 100, 80]

scatter_plot_multiple_data(aData_x,
                      aData_y,
                      sFilename_out,
                      iFlag_miniplot_in = 1,
                      iFlag_scientific_notation_x_in=0,
                      iFlag_scientific_notation_y_in=0,
                      iSize_x_in = None,
                      iSize_y_in = None,
                      iDPI_in = None ,
                      iFlag_log_x_in = None,
                      iFlag_log_y_in = None,
                      dMin_x_in = -1,
                      dMax_x_in = 1,
                      dMin_y_in = -1,
                      dMax_y_in = 1,
                      dSpace_x_in = None,
                      dSpace_y_in = None,
                      sFormat_x_in =None,
                      sFormat_y_in =None,
                      sLabel_x_in ='DRT mesh-based NSE',
                      sLabel_y_in = 'MPAS mesh-based NSE' ,
                         aColor_in=aColor,
                        aMarker_in=aMarker,
                            aSize_in = aSize,
                      aLabel_legend_in = aLabel_legend,
                      sTitle_in = 'Nash-Sutcliffe Efficiency')