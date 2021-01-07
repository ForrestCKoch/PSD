import os
import pickle
import sys
import time

import multiprocessing

sys.path.append('/scratch/yr31/fk5479/psd/PSD/benchmarking')
from datasets import E18MouseData, SimpE18

sys.path.append('/scratch/yr31/fk5479/psd/PSD/')
from psd import psd
import numpy as np
import scipy
from scipy import fft

from memory_profiler import profile

if __name__ == '__main__':

    # this will just be the number of files with size 32k to concatenate
    size=os.environ.get('SIZE')
    rep = os.environ.get('REP')
    large_samples_path = '/scratch/yr31/fk5479/psd/PSD/benchmarking/data/e18_samples/large_samples'
    pickled_files = os.listdir(large_samples_path)

    seed = 100*int(rep)+int(size)
    np.random.seed(seed)
    
    data = np.concatenate([pickle.load(open(os.path.join(large_samples_path,f),'rb')).data for f in np.random.choice(pickled_files,int(size),replace=False)])

    with fft.set_workers(28): 
        start = time.time() 
        psd.psd(data)
        end = time.time()

    with open(os.path.join('/scratch/yr31/fk5479/psd/PSD/benchmarking/results',size+'-'+os.environ.get('REP')+'-largesample-memoryprofiler.txt'),'a') as fh:
        print('Time taken: {}'.format(str(end-start)),file=fh)
