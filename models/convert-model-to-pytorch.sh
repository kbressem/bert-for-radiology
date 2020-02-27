#!/bin/bash

# clone the transformers repository of huggingface (e.g. to documents)

python ../../transformers/convert_bert_original_tf_checkpoint_to_pytorch.py \
   --tf_checkpoint_path='../bert-for-radiology/models/tf-bert-base-german-radiology-cased/pretraining_output/model.ckpt-100000' \
  --bert_config_file='../bert-for-radiology/models/tf-bert-base-german-radiology-cased/rogerbert_config.json' \
  --pytorch_dump_path='../bert-for-radiology/models/pt-bert-base-german-radiology-cased/pytorch-model'

# the -00000-of-00001 in the name of the modelfile, model.ckpt-XXX.data should not be wirtten down when defining the tf_checkpoint_path. Otherwise it will throw the following error: 
# Data loss: not an sstable (bad magic number): perhaps your file is in a different file format and you need to use a different restore operator?

