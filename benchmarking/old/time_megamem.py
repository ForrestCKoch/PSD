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

if __name__ == '__main__':

    with open(os.path.join('/scratch/yr31/fk5479/psd/PSD/benchmarking/data/e18_samples/','GSE93421_'+size+'-sample.pkl'),'rb') as fh:
        x = pickle.load(fh)

    size=os.environ.get('SIZE')
    with fft.set_workers(28): 
        start = time.time() 
        psd.psd(x.data)
        end = time.time()

    with open(os.path.join('/scratch/yr31/fk5479/psd/PSD/benchmarking/results',size+'-'+os.environ.get('REP')+'.txt'),'a') as fh:
        print('Time taken: {}'.format(str(end-start)),file=fh)
