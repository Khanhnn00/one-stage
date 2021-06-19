#!/bin/bash

DATASET=pascal_voc
FILELIST=data/val_voc.txt # validation

## You values here:
#
OUTPUT_DIR= ./results
EXP=baselines
RUN_ID=v1
#
##


LISTNAME=`resnet50_val_voc`

# without CRF
SAVE_DIR= ./results/pascal_voc/baselines/v1/resnet50_val_voc
nohup python eval_seg.py --data ./data --filelist $FILELIST --masks $SAVE_DIR > $SAVE_DIR.eval 2>&1 &

# with CRF
SAVE_DIR=./results/pascal_voc/baselines/v1/resnet50_val_voc/crf
nohup python eval_seg.py --data ./data --filelist $FILELIST --masks $SAVE_DIR > $SAVE_DIR.eval 2>&1 &

# sleep 1

echo "Log: ${SAVE_DIR}.eval"
tail -f $SAVE_DIR.eval
