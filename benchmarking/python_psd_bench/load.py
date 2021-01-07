#!/apps/python/3.7.4/bin/python3 -u
#PBS -l walltime=04:00:00
import sys
import os
sys.path.append(os.environ.get('PBS_O_WORKDIR'))
from datasets import E18MouseData, SimpE18

if __name__ == '__main__':
    print('starting')
    x = SimpE18('/home/z3463797/PSD_Project/PSD/benchmarking/data/GSE93421_brain_aggregate_matrix.hdf5',selection=list(range(0,100000)))
