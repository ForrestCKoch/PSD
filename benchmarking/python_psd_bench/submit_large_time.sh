for i in 2 4 8 16 24; do
    for j in $(seq 1 16); do
        qsub -o logs/timing_largesamples/timing_${i}_${j}-largesample.log -vSIZE=$i,REP=$j time_psd_largesample.sh
    done
done

