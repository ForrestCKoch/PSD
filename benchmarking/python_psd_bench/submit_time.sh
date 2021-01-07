for i in $(ls data/e18_samples/|cut -d'_' -f2|cut -d'-' -f1); do
    for j in $(seq 1 16); do
        qsub -o logs/timing_${i}_${j}.log -vSIZE=$i,REP=$j time_psd.sh
    done
done

