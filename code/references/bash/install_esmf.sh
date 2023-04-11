#!/bin/bash
# installing ESMF on Ubuntu Linux
# pre-req : gfortran, netcdf, openmpi, python3
# first mkdir /opt/esmf/7.0.0 and chown to yourself
# you also need a copy of esmf_7_0_0_src.tar
# Raphael Dussin, July 2016
#https://earthsystemmodeling.org/docs/release/ESMF_5_1_0/ESMF_usrdoc/node6.html

CUSTOMINSTALLDIR=/qfs/people/liao313/private_modules/cplus/esmf/bin

#------------------ installing the ESMF libraries ---------------
module purge
module load gcc/8.1.0
module load openmpi/4.0.1

esmf_folder=/qfs/people/liao313/private_modules/cplus/esmf/esmf
cd $esmf_folder

export ESMF_DIR=$( pwd )
export ESMF_INSTALL_PREFIX=$CUSTOMINSTALLDIR
#export ESMF_COMM=openmpi
#export ESMF_NETCDF=split
#export ESMF_NETCDF_INCLUDE=/usr/include
#export ESMF_NETCDF_LIBPATH=/usr/lib
#export ESMF_NETCDF_LIBS="-lnetcdff -lnetcdf"

make
make install

# At this point you should have ESMF installed
#------------------ installing the python3 wrapper ---------------

#cd ..
#git clone https://github.com/raphaeldussin/ESMPy3.git ESMPy3
#cd ESMPy3
#$PYTHONBIN/python setup.py build --ESMFMKFILE=$CUSTOMINSTALLDIR/lib/libO/Linux.gfortran.64.openmpi.default/esmf.mk install