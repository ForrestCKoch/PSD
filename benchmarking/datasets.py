#!/usr/bin/env python3
###########################################
# This module implements a few classes to 
# help load data into PyTorch compatible 
# datasets.
#
# Although the aim is PyTorch compatibility
# there is no problem in utilizing these
# datasets for general computation
###########################################
from typing import Any, Callable, Optional
from time import time

import numpy as np

from tqdm import tqdm
import h5py
import sharedmem as sm

class SimpE18():

    def __init__(self, 
                 path: str,
                 selection: Optional[list] = None,
                 silent: Optional[bool] = False ) -> None:
        """

        :param path: path to hdf5 file for e18 Mouse Data
        :param selection: list of cells to load data for
        :param silent: whether print statements should print
        """
        hdf5 = h5py.File(path,'r',driver='core')
        self.dims = len(hdf5['mm10']['genes'])
        
        # allow a customizable selection of cells
        if selection is not None:
            self._len = len(selection)
        else:
            self._len = len(hdf5['mm10']['indptr'])
            selection = range(0,self._len)
        
        data = hdf5['mm10']['data']

        indx = hdf5['mm10']['indices']

        iptr = hdf5['mm10']['indptr']
        self.data = np.zeros(shape=(self._len,self.dims))

        ###########################
        # Multi-core loading ...
        ###########################
        if not silent: print("Building Matrix ...")
        start = time()

        for i in range(0,self._len):
            index = i if selection is None else selection[i]

            sidx = iptr[index]
            # find the number of gene entries for
            # this cell
            if index < len(iptr) - 1:
                # find length to next cell
                nentries = iptr[index + 1] - sidx 
            else:
                # find length to the end
                nentries = len(data) - sidx

            for j in range(0,nentries):
                self.data[i][indx[sidx+j]] = (data[sidx+j])

        end = time()

        if not silent: print("\t"+str(end-start)+"s ...")
    
        hdf5.close()
   
    def __getitem__(self, index):
        return np.array(self.data[index])

    def __len__(self):
        return self._len


class E18MouseData():

    def __init__(self, 
                 path: str,
                 log1p: Optional[bool] = False,
                 nproc: Optional[int] = 1,
                 selection: Optional[list] = None,
                 silent: Optional[bool] = False ) -> None:
        """

        :param path: path to hdf5 file for e18 Mouse Data
        :param nproc: number of processes to use in contructing vectors
        :param ratio: ratio of the dataset to actually load
        :param selection: list of cells to load data for
        :param silent: whether print statements should print
        """
        hdf5 = h5py.File(path,'r',driver='core')
        self.dims = len(hdf5['mm10']['genes'])
        
        # allow a customizable selection of cells
        if selection is not None:
            self._len = len(selection)
        else:
            self._len = len(hdf5['mm10']['indptr'])
            selection = range(0,self._len)
        self.selection = selection
        # get a list that can be shared between processes
        selected_cells = sm.empty(self._len,dtype=np.int)
        for i in range(0,self._len):
            selected_cells[i] = self.selection[i]
        
        #self.cells = sm.full((self._len,self.dims),0,dtype=np.int16)
        # Load all of the important information into memory

        #############
        # Data
        #############
        if not silent: print("Reading data ...")
        start = time()

        ds = hdf5['mm10']['data']
        data = sm.empty(len(ds),dtype=ds.dtype)
        ds.read_direct(data)
        tmp = ds.dtype

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")

        #############
        # Indices
        #############
        if not silent: print("Reading indices ...")
        start = time()

        ds = hdf5['mm10']['indices']
        indx = sm.empty(len(ds),dtype=ds.dtype)
        ds.read_direct(indx)

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")

        
        #############
        # Indptr
        #############
        if not silent: print("Reading indptr ...")
        start = time()

        ds = hdf5['mm10']['indptr']
        iptr = sm.empty(len(ds),dtype=ds.dtype)
        ds.read_direct(iptr)

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")

        hdf5.close()
        del ds

        ###########################
        # Create empty cell vectors
        ###########################
        # build the vector foreach cell 
        if not silent: print("Creating 0 vectors ...")
        start = time()

        self.data = sm.full((self._len,self.dims),0,dtype=tmp)
        #self.cells = sm.full((self._len,self.dims),0,dtype=float)
        
        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")
        
        ###########################
        # Multi-core loading ...
        ###########################
        if not silent: print("Building Tensor List ...")
        start = time()
        with sm.MapReduce(np = nproc) as pool:
            pool.map(_build_tensor, list(zip(
                    [self.data] * nproc, [iptr] * nproc,
                    [indx] * nproc, [data] * nproc,
                    range(0,nproc) ,[nproc] * nproc,
                    [selected_cells] * nproc,
                    [log1p] * nproc))
            )

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")
    
        # Some explicit cleanup to conserve memory
        # Not sure if necessary, but I don't trust Python
        del iptr
        del indx
        del data
        del selected_cells
   
    def __getitem__(self, index):
        return np.array(self.data[index])

    def __len__(self):
        return self._len

def _build_tensor(args):
    """
    Helper function to allow parallel loading of tensors 
    """
    cells,iptr,indx,data,tid,nproc,selected,log1p = args

    for i in range(0+tid,len(cells),nproc):
        index = selected[i]
        sidx = iptr[index]
        # find the number of gene entries for
        # this cell
        if index < len(iptr) - 1:
            # find length to next cell
            nentries = iptr[index + 1] - sidx 
        else:
            # find length to the end
            nentries = len(data) - sidx

        for j in range(0,nentries):
            if log1p:
                cells[i][indx[sidx+j]] = np.log(1+(data[sidx+j]))
            else:
                cells[i][indx[sidx+j]] = (data[sidx+j])
            #cells[i][indx[sidx+j]] = float(data[sidx+j])

def scale_dataset(ds):
    """
    Scale each feature to be between 0 and 1
    Note that overwrites the original data.
    In the future, this function should be changed
    to retain scaling information
    
    :param ds: dataset to be scaled
    """
    for i in range(0,ds.dims):
        fmax = ds.data[0][i]
        for j in range(1,len(ds)):
            curr = ds.data[j][i]
            if curr > fmax:
                fmax = curr           
        if fmax > 0:
            for j in range(0,len(ds)):
                ds.data[j][i] /= fmax



if __name__ == '__main__':
    pass
