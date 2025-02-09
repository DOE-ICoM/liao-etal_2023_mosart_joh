
from osgeo import  ogr
import cartopy as cpl
from pyearth.toolbox.data.netcdf.map_netcdf_file import map_netcdf_file
# raw
# set a conversion from mm/day to mm/s




#0.05 degree
iFlag_merged = 1
iFlag_resampled = 1


if iFlag_resampled == 0:
    dResolution = 0.05

    if iFlag_merged == 0:
        conversion = 1.0/86400.0
        sFilename_netcdf_in_path = "/compyfs/liao313/00raw/mingpan_runoff/original/RUNOFF_2019.nc"
        sVariable_in = "ro"
    else:
        conversion = 1.0
        sFilename_netcdf_in_path = "/compyfs/liao313/00raw/mingpan_runoff/sag/ming_daily_2019.nc"
        sVariable_in = "QOVER"  
        pass

    sFolder_output = '/compyfs/liao313/00raw/mingpan_runoff/figures/sag/raw/daily' 

else:
    # resampled
    conversion = 1.0
    dResolution = 0.5
    sFilename_netcdf_in_path = "/compyfs/inputdata/lnd/dlnd7/mingpan/ming_daily_2019.nc"
    sFolder_output = '/compyfs/liao313/00raw/mingpan_runoff/figures/sag/resampled/daily'
    sVariable_in = "QRUNOFF"



aExtent = [-150.015625, -146.234375, 67.921875, 70.328125]
dLongitude_left, dLongitude_right, dLatitude_bot, dLatitude_top = aExtent
pRing = ogr.Geometry(ogr.wkbLinearRing)
pRing.AddPoint(dLongitude_left, dLatitude_top)
pRing.AddPoint(dLongitude_right, dLatitude_top)
pRing.AddPoint(dLongitude_right, dLatitude_bot)
pRing.AddPoint(dLongitude_left, dLatitude_bot)
pRing.AddPoint(dLongitude_left, dLatitude_top)
pBoundary = ogr.Geometry(ogr.wkbPolygon)
pBoundary.AddGeometry(pRing)
pBoundary_wkt = pBoundary.ExportToWkt()
sTitle = 'Total runoff'
sUnit = 'mm/sec'

pProjection_map = cpl.crs.PlateCarree()  # for latlon data only
pProjection_map = None

map_netcdf_file(sFilename_netcdf_in_path,
                sVariable_in,
                iFlag_monthly_in= 0,
                iFlag_daily_in= 1,
                sFolder_output_in=sFolder_output,
                pBoundary_in=pBoundary_wkt,
                iFlag_scientific_notation_colorbar_in=1,
                dData_min_in = 0.0,
                dData_max_in= 1E-4,
                dResolution_x_in=dResolution,
                dResolution_y_in=dResolution,
                dConvert_factor_in=conversion,
                sTitle_in=sTitle,
                sUnit_in=sUnit,
                pProjection_map_in = pProjection_map)
