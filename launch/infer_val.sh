#!/bin/bash

#
# Set your argument here
#
CONFIG=configs/voc_resnet50.yaml
DATASET=pascal_voc
FILELIST=data/test.txt

## You values here (see below how they're used)
#
OUTPUT_DIR= ./results
EXP=baselines
RUN_ID=v1
SNAPSHOT=e012Xs0.902
EXTRA_ARGS=
SAVE_ID=v2
#
##

# limiting threads
NUM_THREADS=6

set OMP_NUM_THREADS=$NUM_THREADS
export OMP_NUM_THREADS=$NUM_THREADS

#
# Code goes here
#
LISTNAME=resnet50_test
SAVE_DIR=./results/pascal_voc/baselines/v2/resnet50_test
LOG_FILE=./results/pascal_voc/baselines/v2/resnet50_test.log

CMD="python infer_val.py --dataset $DATASET \
                         --cfg $CONFIG \
                         --exp $EXP \
                         --run $RUN_ID \
                         --resume $SNAPSHOT \
                         --infer-list $FILELIST \
                         --workers $NUM_THREADS \
                         --mask-output-dir $SAVE_DIR \
                         $EXTRA_ARGS"

if [ ! -d $SAVE_DIR ]; then
  echo "Creating directory: $SAVE_DIR"
  mkdir -p $SAVE_DIR
else
  echo "Saving to: $SAVE_DIR"
fi

# git rev-parse HEAD > ${SAVE_DIR}.head
# git diff > ${SAVE_DIR}.diff
# echo $CMD > ${SAVE_DIR}.cmd

# echo $CMD
# nohup $CMD > $LOG_FILE 2>&1 &

# # sleep 1
# tail -f $LOG_FILE
