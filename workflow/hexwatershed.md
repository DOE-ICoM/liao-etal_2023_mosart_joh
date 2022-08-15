## How to run the HexWatershed model

### Hydroshed flowline post-processing
The filtered flowlines are converted to the GeoJSON format.

### Install the HexWatershed python package

Install the hexwatershed package using Conda (recommended):

        conda install -c conda-forge hexwatershed



### HexWatershed setup

1. Configure the path in the JSON files under the `example` folder.
2. Set up model parameters, e.g., mesh resolution.



### Run simulation

Run the simulations using the `run_susquehanna.py` script using your preferred Python environment.

Correct errors if there are issues in the path configuration.

### Visualization

Two types of output are available under the outpur folder
1. JSON files, contain information of mesh and flowline topological relationship;
2. GeoJSON files, contain conceptual flowlines in the `GIS` format.

### Post-processing

After the MOSART simulations are finished, you can use the HexWatershed utility code to generate the figures.



