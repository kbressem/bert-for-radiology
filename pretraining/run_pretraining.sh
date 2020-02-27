#!/bin/bash

cd ~/Documents/bert-for-radiology/pretraining

# There have been some issues with the linebreaks. If they should persist, delete the '\' and write everything into one line, separating the commands by only one space. 

cd ~/Documents/bert-for-radiology/pretraining
eval "$(conda shell.bash hook)"
conda deactivate
conda activate bert-pretraining

# remove init_checkpoint to train from scratch 

python run_pretraining.py \
  --input_file=../tmp/tf_examples.tfrecord-seq128-* \
  --output_dir=../tmp/pretraining_output \
  --do_train=True \
  --do_eval=True \
  --bert_config_file=../models/bert-base-german-cased/bert_config.json \
  --init_checkpoint=../models/bert-base-german-cased/bert_model.ckpt \
  --train_batch_size=32 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=90000 \
  --num_warmup_steps=9000 \
  --learning_rate=2e-5

# to run additional 10000 steps, the overall num of train_steps needs to be set to 100000 (90000 + 10000 = 100000)

python run_pretraining.py \
  --input_file=../tmp/tf_examples.tfrecord-seq512-* \
  --output_dir=../tmp/pretraining_output \
  --do_train=True \
  --do_eval=True \
  --bert_config_file=../models/bert-base-german-cased/bert_config.json \
  --init_checkpoint=../tmp/pretraining_output/model.ckpt-90000 \
  --train_batch_size=6 \
  --max_seq_length=512 \
  --max_predictions_per_seq=20 \
  --num_train_steps=100000 \
  --num_warmup_steps=91000 \
  --learning_rate=2e-5

