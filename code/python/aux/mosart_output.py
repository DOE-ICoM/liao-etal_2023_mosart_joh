#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 15:20:08 2020

@author: feng779
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from datetime import datetime, timedelta

import pdb


def JDAY_con(JDAY):
    basedate = datetime(2000,1,1)
    return_date = [basedate+timedelta(days = float(ii)) for ii in JDAY]
    return return_date


filename = '../model_output/baseline_GSWP_EC30to60E2r2.2022-03-17-11.mosart.h0.2000-01-02-00000.nc'


nc_output = Dataset(filename, 'r')
lon = nc_output.variables['lon'][:]
lat = nc_output.variables['lat'][:]
MASK = nc_output.variables['MASK']
lonc, latc = np.meshgrid(lon, lat)

#### read mapping file ####
from scipy.sparse import csr_matrix 
#map_file = '../files/map_WC14to60E2r3_to_r0125_nn.210808.nc'
map_file = '../files/map_EC30to60E2r2_to_r0125_nn.220317.nc'
nc_map = Dataset(map_file, 'r')
S = nc_map.variables['S'][:]
col = nc_map.variables['col'][:]
row = nc_map.variables['row'][:]
ndim_a = nc_map.dimensions['n_a'].size  ## rof
ndim_b = nc_map.dimensions['n_b'].size  ## ocn

#### read MPAS-O data  ####
#mpaso_file = '/compyfs/feng779/e3sm_scratch/datm2_yr2002_baseline_GSWP.2021-08-04-23/run/datm2_yr2002_baseline_GSWP.2021-08-04-23.mpaso.hist.am.highFrequencyOutput.2003-06-01_00.00.00.nc'
mpaso_file = '/compyfs/feng779/e3sm_scratch/coupling_test/baseline_GSWP_EC30to60E2r2.2022-03-17-11/run/baseline_GSWP_EC30to60E2r2.2022-03-17-11.mpaso.hist.am.highFrequencyOutput.2000-01-01_00.00.00.nc'
nc_mpaso = Dataset(mpaso_file, 'r')
ssh = nc_mpaso.variables['ssh'][-1,:]

NNear = int(S.size/ndim_b)
W = np.zeros([ndim_b, NNear])
ind = np.zeros([ndim_b, NNear], dtype=int)
for i in range(ndim_b):
    ind[i,:] = col[i*NNear:(i+1)*NNear] - 1
    W[i,:]   = S[i*NNear:(i+1)*NNear]
    
ssh_mosart = np.zeros([ndim_b])

## interpolation here
for i in range(ndim_b):
    ssh_mosart[i] = np.sum(ssh[ind[i,:]]*W[i,:])

ssh_mosart = ssh_mosart.reshape(MASK[0,:,:].shape)


def plotVar(var, varname):

    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    
    cmap = 'bwr'
    
    scale_factor = 1
    var_tstep = var[:,:]
    vmin = var_tstep.min()
    vmax = var_tstep.max()
    levels = np.linspace(-2/scale_factor, 2/scale_factor, 100)
    
    var_masked = var_tstep
    
    cs = ax.contourf(lon, lat, var_masked, cmap=cmap, levels=levels, extend='both')
    
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05)
    cb = fig.colorbar(cs, cax=cax, orientation='vertical')
    cb.ax.tick_params(labelsize=12)
    cb.ax.yaxis.offsetText.set_fontsize(12)
    cb.set_label(varname, fontsize=14)
    
    #timestr = datetime.strftime(model_time[tstep],'%Y-%m-%d')
    #ax.title.set_text('Date: %s'%timestr)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')
    fig.tight_layout()
    #plt.savefig('../figures/ssh_WC14to60E2r3_to_r0125.png')
    plt.savefig('../figures/ssh_EC30to60E2r2_to_r0125.png')
    plt.close()


plotVar(ssh_mosart, 'Sea surface height (m)')
