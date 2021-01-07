for i in 2 4 8 16 24; do
    for j in $(seq 1 4); do
        qsub -o $HOME/results/memory_profiler/largesamples/${i}_${j}.log -vSIZE=$i,REP=$j memory_psd_largesample.sh
    done
done

