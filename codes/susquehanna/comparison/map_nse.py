import os
from pyearth.visual.map.vector.map_vector_point_file import map_vector_point_file
from pyearth.visual.map.pick_colormap import pick_colormap_hydrology
sWorkspace_figure  = '/qfs/people/liao313/workspace/python/liao-etal_2023_mosart_joh/figures/susquehanna'
sFilename_geojson_nse = os.path.join(sWorkspace_figure, 'nse.geojson')

sColormap = pick_colormap_hydrology('nse')
iFiletype_in=1
sFilename_in=sFilename_geojson_nse

sFilename_output_in=sFilename_geojson_nse = os.path.join(sWorkspace_figure, 'nse.png')

aExtent = [-79.10236320495605, -74.35684242248536, 39.374137496948244, 42.9556583404541]

map_vector_point_file(iFiletype_in,
                          sFilename_in,
                          sFilename_output_in= sFilename_output_in,
                          iFlag_openstreetmap_in = 1,
                          iFlag_scientific_notation_colorbar_in=None,
                          sColormap_in=sColormap,
                          sTitle_in='DRT and MPAS mesh-based discharge observation-model comparison',
                          iFlag_zebra_in = 1,
                          iFlag_color_in =1,
                          iFlag_size_in= 1,
                          iFlag_colorbar_in = 1,
                          sField_color_in = 'nse0',
                          sField_size_in = 'nse0',
                          iDPI_in=None,
                          dMissing_value_in=None,
                          dData_max_in=1,
                          dData_min_in=-1,
                          sExtend_in='min',
                          sLocation_legend_in='upper left',
                          sUnit_in='Nash-Sutcliffe Efficiency',
                          aLegend_in=None,
                          aExtent_in =aExtent )
