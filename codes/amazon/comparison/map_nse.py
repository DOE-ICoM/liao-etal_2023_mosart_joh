import os, sys
from osgeo import osr
from pyearth.visual.map.pick_colormap import pick_colormap_hydrology
from pyearth.visual.map.map_servers import calculate_zoom_level, calculate_scale_denominator
sPath_project = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh'
sys.path.append(sPath_project)
from codes.shared.map_vector_point_file import map_vector_point_file

sWorkspace_figure  = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/amazon'
sFilename_geojson_nse = os.path.join(sWorkspace_figure, 'nse.geojson')

sColormap = pick_colormap_hydrology('nse')
iFiletype_in=1
sFilename_in=sFilename_geojson_nse
aExtent= [-80.96294746398925, -48.94024314880371, -21.183916664123537, 6.4270845413208]
sFilename_output_in=sFilename_geojson_nse = os.path.join(sWorkspace_figure, 'nse.png')

image_size = [1000, 1000]
dpi = 300
scale_denominator = calculate_scale_denominator(aExtent, image_size)
pSrc = osr.SpatialReference()
pSrc.ImportFromEPSG(3857) # mercator
pProjection = pSrc.ExportToWkt()
iFlag_openstreetmap_level = calculate_zoom_level(scale_denominator, pProjection, dpi=dpi)
print(iFlag_openstreetmap_level)

map_vector_point_file(iFiletype_in,
                          sFilename_in,
                          sFilename_output_in= sFilename_output_in,
                           iFlag_terrain_image_in = 1,
                          iFlag_openstreetmap_level_in = iFlag_openstreetmap_level,
                          iFlag_scientific_notation_colorbar_in=None,
                          sColormap_in=sColormap,
                          sTitle_in='DRT and MPAS mesh-based discharge observation-model comparison',
                          iFlag_zebra_in = 1,
                          iFlag_color_in =1,
                          iFlag_size_in= 1,
                          iFlag_colorbar_in = 1,
                          sField_color_in = 'nse0',
                          sField_size_in = 'drai',
                          iDPI_in=dpi,
                          dMissing_value_in=None,
                          dData_max_in=1,
                          dData_min_in=-1,
                          sExtend_in='min',
                          sLocation_legend_in='upper left',
                          sUnit_in='Nash-Sutcliffe Efficiency',
                          aLegend_in=None,
                          aExtent_in =aExtent )
