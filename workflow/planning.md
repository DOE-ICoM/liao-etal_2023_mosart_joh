# Planning

## Key points (some overlaps with Chang's other papers

* This paper demonstrates river routing over unstructured mesh within ESM framework
* Compares with traditional lat-long routing scheme. (not aiming to improve routing performance in terms of hydrograph accuracy)
* To hydrology community, this is a novel mesh-independent river routing approach, we are able to burn the river network and points such as dams and gages into the mesh (first time).
* To ESM community, we are building a bridge between ESM and regional modeling by using variable resolution mesh. First time for river processes.


## Experiment design

* Step 1: prepare runoff dataset (Ming Pan) (Depend on step 3)
* Step 2: river network dataset preparation(identify a few basins across spatial scales, with good discharge data). tentatively ICoM basins, one or two Arctic basins, Columbia, and maybe a few large basins on other continents (Need more discussion).

ICoM: 1/16, MPAS

CRB: 1/16,  MPAS

Sag: 1/16, MPAS

Amazon: 1/8, MPAS

* Step 2.5: run pyflowline (optional) stream burning 
* Step 3: MPAS mesh generation (Need more discussion about resolution, w/ or w/o stream burning, etc.)
* Step 4: Run hexwatershed, get river network
* Step 5: Generate MOSART parameter using Donghui’s script
* Step 6: run MOSART over both MPAS and lat-long configurations
* Step 7: Analyses (Need more discussion about metrics, etc.)
