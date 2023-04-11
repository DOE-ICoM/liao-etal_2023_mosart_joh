## mapping file

### domain file

1/16 domainf file
mpas domain file


export DST=/global/cfs/cdirs/e3sm/inputdata/lnd/clm2/mappingdata/grids/MOSART_global_8th.scrip.20180211c.nc
export SRC=/project/projectdirs/e3sm/inputdata/lnd/clm2/mappingdata/grids/SCRIPgrid_0.5x0.5_AVHRR_c110228.nc
export EXE=/project/projectdirs/ccsm1/esmf/cori/ESMF-7.1.0r-netcdf-hdf5parallel-intel18.0.1.163-mpi-O-cori-knl/bin/binO/Unicos.intel.64.mpi.default//ESMF_RegridWeightGen
srun -n 24 $EXE --ignore_unmapped -s $SRC -d $DST -w map.nc -m conserve