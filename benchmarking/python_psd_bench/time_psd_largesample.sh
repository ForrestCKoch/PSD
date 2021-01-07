#!/bin/sh
#PBS -q hugemembw
#PBS -l walltime=04:00:00
#PBS -l wd
#PBS -l mem=800gb
#PBS -l ncpus=28
#PBS -v SIZE,REP
#PBS -j oe
#PBS -P yr31

export OMP_NUM_THREADS=$PBS_NCPUS
module load python3/3.8.5
python3 time_psd_largesample.py
