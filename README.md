
# Liao. et al. 2024 Journal of Advances in Modeling Earth Systems

**Evaluation of flow routing on the unstructured Voronoi meshes in earth system modeling**

Chang Liao<sup>1\*</sup>,
Donghui Xu<sup>1</sup>,
Matt Cooper<sup>1</sup>,
Tian Zhou<sup>1\*</sup>,
Darren Engwirda<sup>2</sup>,
Zeli Tan<sup>1\*</sup>,
Gautam Bisht<sup>1</sup>,
Hong-Yi Li<sup>3</sup>,
Lingcheng Li<sup>1\*</sup>,
Dongyu Feng<sup>1\*</sup>,
and L. Ruby Leung<sup>1</sup>

<sup>1 </sup> Atmospheric Sciences and Global Change, Pacific Northwest National Laboratory, Richland, WA, USA

<sup>2 </sup> T-3 Fluid Dynamics and Solid Mechanics Group, Los Alamos National Laboratory, Los Alamos, NM, USA

<sup>3 </sup> University of Houston, Houston, TX, USA


\* corresponding author:  chang.liao@pnnl.gov; tian.zhou@pnnl.gov

## Abstract

Flow routing is a fundamental process of Earth System Models' (ESMs) river component. Traditional flow routing models rely on Cartesian rectangular meshes, which exhibit limitations, particularly when coupled with unstructured mesh-based ocean components. They also lack the support for regionally refined models (RRMs).
While previous studies have highlighted the potential benefits of unstructured meshes for flow routing, their widespread application and comprehensive evaluation within ESMs remain limited. This study extends the river component of the Energy Exascale Earth System Model (E3SM) to unstructured Voronoi meshes. We evaluated the model's performance in simulating river discharge and water depth across three watersheds spanning the Arctic, temperate, and tropical regions. The results show that while providing several benefits, unstructured mesh-based flow routing can achieve comparable performance to structured mesh-based routing, and their difference is often less than 10%. Although the unstructured mesh-based method could address several existing limitations, this research also shows that additional improvements in the numerical method are needed to fully exploit the advantages of unstructured mesh for hydrologic and ESMs.

## Journal reference
Liao. et al. (2024). Evaluation of flow routing on the unstructured Voronoi meshes in earth system modeling.

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


