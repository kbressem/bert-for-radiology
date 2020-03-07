# Classification of Radiological Text Reports using BERT

## Data Preparation
### Extraction of Free Text Reports
Single plain text files were stored on a network-drive. File-names and paths were prior extracted using R `list.files()` function and stored in one very large table. As the workstation used by us has >120 GB RAM, keeping such large files in memory is no problem. On Coimputers with smaller memory some workarrounds might be needed.   

used script: [text-extraction/extract-reports.R](text-extraction/extract-reports.R)

### Clean Text Dump
About one million reports are not usable, since they only document DICOM-imports, meetings, consistency tests or the like. These were removed by full and partial string matching. In this way, it was possible to remove a large part of the inappropriate diagnostic texts and reducing the number of text-reports from 4,790,000 to 3,841,543. 

used scripts:   
[text-extraction/clean-report-texts.R](text-extraction/clean-report-texts.R)

### Converting the Texts to Document Format
For generation of a custom vocabulary and for generation of training-data for BERT, the source-files need to be in a specific document format which is: 

> "The input is a plain text file, with one sentence per line. (It is important that these be actual sentences for the "next sentence prediction" task). Documents are delimited by empty lines."

As all text files were stored as csv, they need to be converted to document format. Each row did contain a document, therefore pasting the empty line between documents was straightforward, however having only one sentence per line requires the documents to be split by sentence, which is more complicated.  
In order to sentencize the reports the German nlp-module of `spaCy` was used. As this did not work perfectly and also split most of the radiology-specific abbreviations an other function to fix those wrong splits was written. 

A [notebook](pretraining/sentencizing.ipynb) on the process and a [python-script](pretraining/run_sentencizing.py) to run the code from the bash can be found in the folder pregeneration.

### Create WordPiece vocabulary
Google research does not provide scripts to create a new WordPiece vocabulary. They do refer to other open source options such as:

- [Google's SentencePiece library](https://github.com/google/sentencepiece)
- [tensor2tensor's WordPiece generation script](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/text_encoder_build_subword.py)
- [Rico Sennrich's Byte Pair Encoding library](https://github.com/rsennrich/subword-nmt)

But, as they mentoin, these are not compatible with their `tokenization.py` library. Therefore we used the modified library by [kwonmha](https://github.com/kwonmha/bert-vocab-builder) to build a custom vocabulary. 

A [notebook](pretraining/bert-custom-vocabulary.ipynb) explaining the steps neseccary to create a custom WordPiece vocabulary can be found in the folder pretraining. 

### Create Pretraining Data
The `create_pretraining_data.py` script form Google was used. Due to memory limitations, the text dump had to be split into smaller parts. The [Notebook](pretraining/notebooks/03_create-pretraining-data.ipynb) gives more details on the procedure of data-preparation.  

### Run Pretraining
Two models were pretrained using the BERT base configuraton. One was pretrained from scratch, one using a German BERT Model as initial Checkpoint. The [Notebook](pretraining/notebooks/04_run-pretraining.ipynb) explains pretraining in more detail. 

## Finetuning of four different BERT models
The german BERT Model from deepset.ai, the multilingual BERT model from Google, and our two pretrained BERT models were all fintuned on varing ammounts of annotated text reports of chest radiographs. 
The steps of the fine-tuning process are explained in detail in the respective [notebooks](finetuning). 

## Results
Our BERT models achieve state of the art performance compared to the existing literature. 

| F1- scores 		| RAD-BERT	| RAD-BERT train size=1000 | [Olatunji et al.  2019](https://arxiv.org/pdf/1905.02283.pdf) | [Reeson et al.  2018](https://www.ncbi.nlm.nih.gov/pubmed/29802131) |	[Friedlin et al.  2006](https://www.ncbi.nlm.nih.gov/pubmed/17238345) |	[Wang et al.   2017](https://arxiv.org/abs/1705.02315) |	MetaMap $   2017 |	[Asatryan et al.  2011](https://www.ncbi.nlm.nih.gov/pubmed/21093355) |	[Elkin et al.  2008](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2656026/) |   
|---|---|---|---|---|---|---|---|---|---|---|  
| Globally abnormal 	|	0.96  |	0.96	| 0.83		  | na 		| na 	|	0.93+ 		|0.91+ 			| na 		| na 		|  
| Cardiomegaly      	| na 	| na 	|	0.23      | na 	|	0.97	| 0.88 			|	0.9 		| na 		| na 		|  
| Congestion        	|	0.9	| 0.86 		| na 	  | na 	|	0.98	| 0.83§ 		|	0.77§ 		|	 na 	| na 		|  
| Effusion 	    	|	0.92	| 0.92 		|  na 	  | na 	|	0.98 	|	0.87		| 0.81 			| na 		| na 		|  
| Opacity/Consolidation |	0.92 	|	0.88 	|	0.63 	  | na 	| na 	| 0.91/0.80/0.77\# 	|	0.95/0.39/0.71\# |	0.24-0.57\* 	|	0.82 		|  
| Pneumothorax    	|	0.89    |	0.79	| na 		  |	0.92	| na 		|	0.86		| 0.46 			| na 		| na		|   
| Venous catheter  	|	0.98    |	0.96 	| na 	  |	0.97 	| na 	| na 		| na 		| na 		| na		|   
| Thoracic drain   	|	0.95    |	0.9	| na 		  |	0.95 	| na 	| na 		| na 		| na 		| na 		|  
| Medical devices  	|	0.99    |	0.99	| 0.29 		  | na 	| na 	| na 		| na 		| na 		| na 		|  
| Best F1-score    	|	0.99    |	0.99 	|	0.83 	  | 	0.95 	|	0.98 	|	0.93 		|	0.95 		|	0.57		| 0.82 			|  
| Worst F1-score   	|	0.58	| 0.4 		|	0.23 	  | 	0.92	| 0.97		| 0.52			| 0.39			| 0.24			| 0.82 			|  

\+ detection of normal radiographs  
\# Consolidation/Opacity was not reported but atelectasis, infiltration and pneumonia  
\$ As reported by Wang et al.34 
\§ Congestion not reported, but edema.  
\* performed only pneumonia detection, as a clinical diagnosis and used varying thresholds of pneumonia-prevalence.  
_na_ not available/not reported by study
