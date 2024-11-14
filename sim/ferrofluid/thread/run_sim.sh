#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_amp=0.05
MAX_amp=0.15
amp_STEP=0.05

MIN_nd=3.25
MAX_nd=4.0
nd_STEP=0.25

MIN_NS=1
MAX_NS=5
NS_STEP=1


N_CPU=4   # For each simulation
N_MAX=3   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for amp in $(seq ${MIN_amp} ${amp_STEP} ${MAX_amp})
do
  mkdir $amp

  for nd in $(seq ${MIN_nd} ${nd_STEP} ${MAX_nd})
  do
    mkdir $amp/$nd
    
    for ns in $(seq ${MIN_NS} ${NS_STEP} ${MAX_NS})
    do
      
      DIR=$amp/$nd/$ns
      mkdir $DIR
      
      mpirun -n $N_CPU lmp_py -in thread.lmp -var DIR $DIR -var Amp $amp -var FieldNDrops $nd -var seed $ns > $DIR/bash.out &
      echo "Running simulation on $DIR"
      echo
      if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi
      
    done
  done
done

wait
