import pandas as pd
import numpy as np
import folium
import os
from branca.element import Template, MacroElement

## this script is to generate an interactive map as an html file.
## Step1, execute a matlab script to extract the data from the MOSART output, and produce plots for each gauge location
## This step will also generate metrics for each gauge and put them into an .csv file
## Step2, execute this script to read the matlab generated .csv file, and link the interactive map to the gauge plots

# Function to map NSE values to colors
def nse_to_color(nse, nse_min=-1, nse_max=1):
    if nse <= nse_min:
        return '#000000'  # Black for NSE <= -1
    elif nse < 0:
        # Interpolate from red to white as NSE goes from -1 to 0
        red = 255
        green_blue = int(255 * (nse - nse_min) / -nse_min)
        return f'#{red:02x}{green_blue:02x}{green_blue:02x}'
    elif nse == 0:
        return '#FFFFFF'  # White for NSE = 0
    else:
        # Interpolate from white to blue as NSE goes from 0 to 1
        blue = 255
        red_green = int(255 * (1 - nse) / nse_max)
        return f'#{red_green:02x}{red_green:02x}{blue:02x}'

# Define a function to determine the edge color
def get_edge_color(nse, nse_min=-1, nse_max=1):
    if nse <= nse_min:
        return '#000000'  # Black for NSE <= -1
    else:
        return 'blue' if nse > 0 else 'red'

# Function to integrate plots with the map
def integrate_plots_with_map(df, base_path, plots_directory):
    # map_center = [df['Lat (model)'].mean(), df['Lon (model)'].mean()]
    map_center = [10, 0]
    map = folium.Map(location=map_center, zoom_start=3)

    # Set tile layer with no_wrap
    # folium.TileLayer('cartodbpositron').add_to(map)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri'
    ).add_to(map)

    # Adding Esri Hydro Reference Overlay
    esri_hydro = folium.TileLayer(
        tiles='https://tiles.arcgis.com/tiles/P3ePLMYs2RVChkJx/arcgis/rest/services/Esri_Hydro_Reference_Overlay/MapServer/tile/{z}/{y}/{x}',
        attr='Esri Hydro Reference',
        name='Esri Hydro Reference Overlay',
        overlay=True
    )
    esri_hydro.add_to(map)

    # Determine the minimum size for a marker
    min_size = 1
    for _, row in df.iterrows():
        gauge_id = row['ID']
        river_name = row['River']
        tooltip_text = f"River: {river_name}"
        plot_path = os.path.join(base_path, plots_directory, f"{gauge_id}.png")
        iframe = folium.IFrame(f'<img src="{plot_path}" style="width:100%; height:auto;">', width=400, height=400)
        popup = folium.Popup(iframe, max_width=520)

        color = nse_to_color(row['NSE'])
        edge_color = get_edge_color(row['NSE'])

        # Calculate marker size using logarithmic scale
        # Add a small value to avoid log(0) and log(negative) issues
        size = np.log(row['Annual meanQ obs'] + 1) * min_size * 1.5

        folium.CircleMarker(
            location=[row['Lat (model)'], row['Lon (model)']],
            popup=popup,
            tooltip=tooltip_text,
            radius = size,
            color=edge_color,
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(map)

    return map

# Base path and plots directory
dirname = '2024_Tutorial'
casename = 'GRFR'
www_root = "https://portal.nersc.gov/cfs/e3sm/tizhou/"
www_path = www_root + dirname + "/" + casename + "/"
diag_root = "P:\\global\\cfs\\cdirs\\e3sm\\www\\tizhou\\"
diag_path =  diag_root + dirname + "\\" + casename + "\\"
plots_directory = "gauge_plots"

# CSV file path under the case path
csv_file_path = os.path.join(www_path, "gauge_data.csv")

# Read the gauge data from CSV
df = pd.read_csv(csv_file_path)

# Generate the map
my_map = integrate_plots_with_map(df, www_path, plots_directory)

# HTML and CSS template for the legend
legend_html = '''
