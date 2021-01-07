for i in $(ls data/e18_samples/|cut -d'_' -f2|cut -d'-' -f1); do
    for j in $(seq 1 4); do
        qsub -o results/memory_profiler/memory_${i}_${j}.log -vSIZE=$i,REP=$j memory_psd.sh
    done
done

