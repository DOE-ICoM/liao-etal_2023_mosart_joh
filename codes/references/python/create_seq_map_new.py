#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:58:40 2021

@author: feng779
"""

from netCDF4 import Dataset
import numpy as np
from datetime import datetime
import os
import time

import pdb

class create_seq_map(object):
    
    """
    class that creates a new ocn->rof mapping file from previous rof->ocn mapping file 
    
    consider using ncremap in the future:
        http://nco.sourceforge.net/nco.html#ncremap-netCDF-Remapper
    """
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        
    def read_rof2ocn(self, rof2ocn_file):
        """
        read rof->ocn mapping file 
        
        Example: 
            domain_a: /lustre/scratch3/turquoise/jonbob/ACME/inputTree/acme/inputdata/rof/mosart/MOSART_Global_half_20161014c.nc
            domain_b: /users/jonbob/grids/SCRIP_files/ocean.QU.480km.scrip.151209.nc
        
        dimensions:
            n_a(259200), ni_a(720), nj_a(360), nv_a(4), src_grid_rank(2)
            n_b(1791),   ni_b(1791),nj_b(1),   nv_b(6), dst_grid_rank(2)
            n_s(259200)
            
        variables: 
            rof:
            xc_a(n_a), yc_a(n_a), xv_a(n_a,nv_a), yv_a(n_a,nv_a), mask_a(n_a), area_a(n_a), frac_a(n_a), 
            src_grid_dims(src_grid_rank)
            ocn:
            xc_b(n_b), yc_b(n_b), xv_b(n_b,nv_b), yv_b(n_b,nv_b), mask_b(n_b), area_b(n_b), frac_b(n_b),
            dst_grid_dims(dst_grid_rank)
            sparse matrix
            S(n_s), col(n_s), row(n_s)
        """
        
        self.rof2ocn_file = rof2ocn_file
        
        nc = Dataset(rof2ocn_file, 'r')
        #print (nc)
        # https://en.wikipedia.org/wiki/Sparse_matrix
        self.ndim_a = nc.dimensions['n_a'].size  ## rof
        self.ndim_b = nc.dimensions['n_b'].size  ## ocn
        
        self.xc_a = nc.variables['xc_a'][:]
        self.yc_a = nc.variables['yc_a'][:]
        
        self.xc_b = nc.variables['xc_b'][:]
        self.yc_b = nc.variables['yc_b'][:]
        
        self.mask_a = nc.variables['mask_a'][:]
        self.mask_b = nc.variables['mask_b'][:]
        
        self.S = nc.variables['S'][:]
        self.col = nc.variables['col'][:]
        self.row = nc.variables['row'][:]
        
    def readMask(self, mask_file):
        """
        read mask info from mosart output
        MOSART mask 1=land 2=ocean 3=outlet
        """
        nc = Dataset(mask_file)
        #print (nc)
        self.mask = nc.variables['MASK'][0,:,:].reshape(self.ndim_a, order='A')
        #pdb.set_trace()
        
            
    def sparse_matrix_interp(self, add_mask=False, mask_file=None):
        """
        create sparse_matrix for interpolation
        """
        from scipy import spatial, sparse
        
        starttime = time.time()
        ## rof grid
        ## first make index consistent for interpolation
        self.xc_a = self.xc_a % 360
        #self.xc_a[self.xc_a<=0] += 360
        xcyc_a = np.vstack([self.xc_a.ravel(), self.yc_a.ravel()]).T
        
        ## ocn grid
        xcyc_b = np.vstack([self.xc_b.ravel(), self.yc_b.ravel()]).T
        
        ## Nearest Neighbor
        maxdist=np.inf
        NNear = 2   # Number of points to include in interpolation (only applicable to idw and kriging)
        p = 1.0     # power for inverse distance weighting
        eps = 1e-10 # This avoids 0 denominator
        
        kd = spatial.cKDTree(xcyc_b)
        # Perform query on all of the points in the grid
        dist, ind=kd.query(xcyc_a,distance_upper_bound=maxdist, k=NNear)
        # Calculate the weights
        W = 1/(dist+eps)**p
              
        
        self.S_new = np.zeros([self.ndim_a*NNear])
        self.col_new = np.zeros([self.ndim_a*NNear], dtype=int)
        if NNear == 1:
            print ("NNear=", 1)
            for i in range(self.ndim_a):
                self.S_new[i*NNear:(i+1)*NNear] = 1.
                self.col_new[i*NNear:(i+1)*NNear] = ind[i] + 1
            
        elif NNear > 1:
            print ("NNear=", NNear)
            Wsum = np.sum(W,axis=1)  
            for ii in range(NNear):
                W[:,ii] = W[:,ii]/Wsum            
        
            for i in range(self.ndim_a):
                self.S_new[i*NNear:(i+1)*NNear] = W[i,:]
                self.col_new[i*NNear:(i+1)*NNear] = ind[i,:] + 1 # adjust index, fortran index starts from 1
                
        ## create the mask
        #mask = (dist==np.inf)
        #ind[mask]=1
        if add_mask:
            self.readMask(mask_file)
            if NNear == 1:
                self.S_new[np.where(self.mask==1)] = 0.
            else:
                for i in range(NNear):
                    self.S_new[i::2][np.where(self.mask==1)] = 0.
                
        
        self.n_s = self.S_new.size
        self.row_new = np.arange(1, self.ndim_a+1)
        self.row_new = np.repeat(self.row_new, NNear)
        
        
        endtime = time.time()
        print ('Sparse matrix creation time: ', endtime-starttime)
        pdb.set_trace()
        
    
    def create_ocn2rof(self, ocn2rof_file):
        """
        create ocn->rof mapping file
        """
        import getpass
        
        if os.path.exists(ocn2rof_file):
            os.remove(ocn2rof_file)
        
        nc_in = Dataset(self.rof2ocn_file, 'r')
        nc_out = Dataset(ocn2rof_file, 'w', format='NETCDF3_CLASSIC')
        
        #### Deinf global attributes    ####
        user_name = getpass.getuser()
        setattr(nc_out,'Created_by',user_name)
        setattr(nc_out,'Created_on',datetime.now().strftime('%c'))
        nc_attrs = nc_in.ncattrs()
        for nc_attr in nc_attrs:
            if nc_attr == 'domain_a':
                setattr(nc_out, nc_attr, nc_in.getncattr('domain_b'))
            elif nc_attr == 'domain_b':
                setattr(nc_out, nc_attr, nc_in.getncattr('domain_a'))
            else:
                setattr(nc_out, nc_attr, nc_in.getncattr(nc_attr))
        
        #### Define nc dimensions       ####
        for dimname in nc_in.dimensions:
            if dimname == 'n_a':
                nc_out.createDimension(dimname,len(nc_in.dimensions['n_b']))
            elif dimname == 'ni_a':
                nc_out.createDimension(dimname,len(nc_in.dimensions['ni_b']))
            elif dimname == 'nj_a':
                nc_out.createDimension(dimname,len(nc_in.dimensions['nj_b']))
            elif dimname == 'nv_a':
                nc_out.createDimension(dimname,len(nc_in.dimensions['nv_b']))
            elif dimname == 'src_grid_rank':
                nc_out.createDimension(dimname,len(nc_in.dimensions['dst_grid_rank']))
            elif dimname == 'n_b':
                nc_out.createDimension(dimname,len(nc_in.dimensions['n_a']))
            elif dimname == 'ni_b':
                nc_out.createDimension(dimname,len(nc_in.dimensions['ni_a']))
            elif dimname == 'nj_b':
                nc_out.createDimension(dimname,len(nc_in.dimensions['nj_a']))
            elif dimname == 'nv_b':
                nc_out.createDimension(dimname,len(nc_in.dimensions['nv_a']))
            elif dimname == 'dst_grid_rank':
                nc_out.createDimension(dimname,len(nc_in.dimensions['src_grid_rank']))
            elif dimname == 'n_s':
                nc_out.createDimension(dimname,self.n_s)
            else:
                raise IOError('This dimension is not available!')
        
        #### Define nc variables        ####
        var = dict()
        for varname in nc_in.variables:
            dtype = nc_in.variables[varname].dtype
            dims  = nc_in.variables[varname].dimensions
            var[varname] = nc_out.createVariable(varname, dtype, dims)
            for ncattr in nc_in.variables[varname].ncattrs():
                attr = nc_in.variables[varname].getncattr(ncattr)
                setattr(var[varname], ncattr, attr)
         
        
        #### Assign variable values    ####
        for varname in nc_out.variables:
            #### domain a ####
            if varname == 'xc_a':
                var[varname][:] = nc_in.variables['xc_b'][:]
            elif varname == 'yc_a':
                var[varname][:] = nc_in.variables['yc_b'][:]
            elif varname == 'xv_a':
                var[varname][:] = nc_in.variables['xv_b'][:] 
            elif varname == 'yv_a':
                var[varname][:] = nc_in.variables['yv_b'][:] 
            elif varname == 'mask_a':
                var[varname][:] = nc_in.variables['mask_b'][:] 
            elif varname == 'area_a':
                var[varname][:] = nc_in.variables['area_b'][:] 
            elif varname == 'frac_a':
                var[varname][:] = nc_in.variables['frac_b'][:] 
            elif varname == 'src_grid_dims':
                var[varname][:] = nc_in.variables['dst_grid_dims'][:] 
                
            #### domain b ####
            elif varname == 'xc_b':
                var[varname][:] = nc_in.variables['xc_a'][:] 
            elif varname == 'yc_b':
                var[varname][:] = nc_in.variables['yc_a'][:] 
            elif varname == 'xv_b':
                var[varname][:] = nc_in.variables['xv_a'][:]
            elif varname == 'yv_b':
                var[varname][:] = nc_in.variables['yv_a'][:] 
            elif varname == 'mask_b':
                var[varname][:] = nc_in.variables['mask_a'][:] 
            elif varname == 'area_b':
                var[varname][:] = nc_in.variables['area_a'][:] 
            elif varname == 'frac_b':
                var[varname][:] = nc_in.variables['frac_a'][:] 
            elif varname == 'dst_grid_dims':
                var[varname][:] = nc_in.variables['src_grid_dims'][:]
                
            #### sparse matrix ####
            elif varname == 'S':
                var[varname][:] = self.S_new
            elif varname == 'col':
                var[varname][:] = self.col_new
            elif varname == 'row':
                var[varname][:] = self.row_new
            
        
        nc_out.close()
        
    
            
        
def print_ncattr(nc_fid, key):
    """
    Prints the NetCDF file attributes for a given key

    Parameters
    ----------
    key : unicode
    a valid netCDF4.Dataset.variables key
    """
    try:
        print ("\t\ttype:", repr(nc_fid.variables[key].dtype))
        for ncattr in nc_fid.variables[key].ncattrs():
            print ('\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr)) )
    except KeyError:
        print ("\t\tWARNING: %s does not contain variable attributes" % key )
        
        
        
if __name__ == "__main__":
    CSM = create_seq_map()
    #rof2ocn_file = '/Users/feng779/OneDrive - PNNL/Documents/CODE/Coupling/interpolation/files/map_r05_to_oQU480_nn.180702.nc'
    #rof2ocn_file = '/Users/feng779/OneDrive - PNNL/Documents/CODE/Coupling/interpolation/files/map_r05_to_EC30to60E2r2_smoothed.r150e300.201005.nc'
    #rof2ocn_file = '/qfs/people/feng779/PYTHON/interpolation/files/map_r0125_to_WC14to60E2r3_smoothed.r150e300.200929.nc'
    rof2ocn_file = '/qfs/people/feng779/PYTHON/interpolation/files/map_r0125_to_EC30to60E2r2_smoothed.r150e300.210311.nc'
    CSM.read_rof2ocn(rof2ocn_file)
    
    #mask_file = '/Users/feng779/OneDrive - PNNL/Documents/CODE/Coupling/smallTrigrid_coupler_test.2021-01-22-21/files/smallTrigrid_monthly.2021-01-26-16.mosart.h0.0001-02.nc'
    #mask_file = '/qfs/people/feng779/PYTHON/interpolation/model_output/datm2_yr2002_baseline_GSWP.2021-08-04-23.mosart.h0.2002-01-02-00000.nc'
    mask_file = '/qfs/people/feng779/PYTHON/interpolation/model_output/baseline_GSWP_EC30to60E2r2.2022-03-17-11.mosart.h0.2000-01-02-00000.nc'
    CSM.sparse_matrix_interp(add_mask=True,mask_file=mask_file)
    
    #ocn2rof_file = 'files/map_oQU480_to_r05_nn_masked.210323.nc'
    #ocn2rof_file = 'files/map_EC30to60E2r2_to_r05_nn.210304.nc'
    #ocn2rof_file = 'files/map_EC30to60E2r2_to_r05_nn_masked.210324.nc'
    #ocn2rof_file = 'files/map_WC14to60E2r3_to_r0125_nn.210808.nc'
    ocn2rof_file = 'files/map_EC30to60E2r2_to_r0125_nn.220317.nc'
    CSM.create_ocn2rof(ocn2rof_file)
    
        
