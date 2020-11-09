#!/apps/python3/3.7.4/bin/python3
#PBS -l walltime=04:00:00
#PBS -l wd
#PBS -l mem=16gb
#PBS -l ncpus=4
#PBS -v DATASET
#PBS -j oe
#PBS -o /home/561/fk5479/PSD_test.log
#PBS -P yr31
#PBS -M forrest.c.koch@gmail.com
#PBS -m be
import os
import pickle
import sys
import time

sys.path.append('/scratch/yr31/fk5479/psd/PSD/benchmarking')
from datasets import E18MouseData, SimpE18

sys.path.append('/scratch/yr31/fk5479/psd/PSD/')
from psd import psd

if __name__ == '__main__':

    with open(os.environ.get('DATASET'),'rb') as fh:
        x = pickle.load(fh)
    
    start = time.time() 
    psd.psd(x.data)
    end = time.time()
    print('Time taken: {}'.format(str(end-start)))
