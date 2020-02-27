# Explanation of files

_vocab-bert-mincount-1000.txt_  
WordPiece vocabulary. Not further processed. Flag for min_count was set to 1000. 

_vocab-bert-mincount-1000-handcleaned.txt_  
WordPiece vocabulary. Special characters have been removed form tokens (e.g. '(Serie' --> 'Serie'). The same token may appear multiple times. 

_vocab-bert-mincount-5000.txt_
WordPiece vocabulary. Not further processed. Flag for min_count was set to 5000. 

_vocab-bert-handcleaned-30000.txt_
Further processed _vocab-bert-mincount-1000-handcleaned.txt_, double tokes have been replaced, `[unusedX]` tokens were inserted to fill the vocabulary up to 30000. 
