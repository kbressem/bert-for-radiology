#!/bin/bash
printf "\033c"

eval "$(conda shell.bash hook)"
conda activate bert-vocab


# define variables
i=0
datadir='../data/small-splits/'
outdir128='../tmp/tf_examples.tfrecord-seq128-'
outdir512='../tmp/tf_examples.tfrecord-seq512-'
vocabdir='../wordpiece-vocabularies/vocab-bert-handcleaned-30000.txt'
splits=$(ls $datadir)

# run the loop
for FILE in $splits
do
	i=$((i+1))

	python create_pretraining_data.py \
	   --input_file="$datadir$FILE" \
	   --output_file="$outdir128${i}" \
	   --vocab_file="$vocabdir" \
	   --do_lower_case=False \
	   --max_seq_length=128 \
	   --max_predictions_per_seq=20 \
	   --masked_lm_prob=0.15 \
	   --random_seed=12345 \
	   --dupe_factor=5

	python create_pretraining_data.py \
	   --input_file="$datadir$FILE" \
	   --output_file="$outdir512${i}" \
	   --vocab_file="$vocabdir" \
	   --do_lower_case=False \
	   --max_seq_length=512 \
	   --max_predictions_per_seq=20 \
	   --masked_lm_prob=0.15 \
	   --random_seed=12345 \
	   --dupe_factor=5
	printf "\033c"

done

