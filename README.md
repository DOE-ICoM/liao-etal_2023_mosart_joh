
# Liao. et al. 2022 Journal of Hydrology

**Evaluation of river routing on a unstructured mesh for coupled earth system modeling**

Chang Liao<sup>1\*</sup>, 
Donghui Xu<sup>1</sup>,
Darren Engwirda<sup>2</sup>, 
Matt Cooper<sup>1</sup>,
Tian Zhou<sup>1\*</sup>,
Gautam Bisht<sup>1</sup>,
Hong-Yi Li<sup>3</sup>,
Ning Sun<sup>1</sup>,
and L. Ruby Leung<sup>1</sup>

<sup>1 </sup> Atmospheric Sciences and Global Change, Pacific Northwest National Laboratory, Richland, WA, USA

<sup>2 </sup> T-3 Fluid Dynamics and Solid Mechanics Group, Los Alamos National Laboratory, Los Alamos, NM, USA

<sup>3 </sup> University of Houston, Houston, TX, USA

\* corresponding author:  chang.liao@pnnl.gov; tian.zhou@pnnl.gov

## Abstract

Spatial discretization is critical in robustly modeling spatially distributed hydrologic processes, particularly runoff routing. Flow routing models that use a Cartesian grid have several limitations including inconstancy in travel time in different directions, inaccurate representation of watershed boundary with sharp corners, and lacking of interface connection between land and ocean in Earth Systems Models (ESMs), in which ocean models routinely use a variable-resolution Voronoi grid. The different types of grids used by the river, land and ocean components in ESMs leads to significant challenges in capturing river-land-ocean continuum. Earlier studies have suggested that use of a hexagonal grid within flow routing models has the potential to resolve aforementioned limitations, yet the applications of such grids are rare in ESMs. In this study, we extend MOSART, the flow routing model of the Energy Exascale Earth System Model (E3SM), to use a hexagonal grid. We evaluate MOSART simulation that use hexagonal and cartesian grids against multiple observational datasets and compare the performance at multiple spatial resolutions. This study improves our understanding of the impacts of spatial discretization on flow routing model performance and the corresponding uncertainties. It also paves the way to better coupling river, land and ocean components in ESMs. 

## Journal reference
Liao. et al. (2022). Evaluation of river routing on a unstructured grid for coupled earth system modeling. 

## Code reference

References for each minted software release for all code involved.  

Liao, Chang, & Cooper, Matt. (2022). Pyflowline: a mesh-independent river networks generator for hydrologic models (0.1.22). Zenodo. https://doi.org/10.5281/zenodo.6604337

Liao, Chang. (2022). HexWatershed: a mesh independent flow direction model for hydrologic models (0.1.12). Zenodo. https://doi.org/10.5281/zenodo.6551861


## Data reference

### Input data
Reference for each minted data source for your input data.  For example:



### Output data
Reference for each minted data source for your output data.  For example:



## Contributing modeling software

| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| PyFlowline | version | https://doi.org/10.5281/zenodo.6604337 | link to DOI dataset |
| HexWatershed | version | https://doi.org/10.5281/zenodo.6551861 | link to DOI dataset |


## Reproduce my experiment

You need to follow three major steps to reproduce this study: 

1. Run the [MPAS model](https://github.com/DOE-ICoM/mpas_mosart/blob/main/workflow/jigsaw_mpas.md)
2. Run the [HexWaterhshed model](https://github.com/DOE-ICoM/mpas_mosart/blob/main/workflow/hexwatershed.md)
3. Run the [MOSART model](https://github.com/DOE-ICoM/mpas_mosart/blob/main/workflow/mosart.md)



## Reproduce my figures

Use the scripts found in the `figures` directory to reproduce the figures used in this publication.


