library(tidyverse)

# this script can be used to insert new vocabs in an existing WordPiece vocabulary, in place of "unused" token 
# It is currently not used for models in this repository, as a new WordPiece vocabulary was generated. 

EXISTING_VOCABS = "vocab.txt"  # path to the WordPiece vocab file to be changed
VOCABS_TO_INSERT = "vocabs-to-insert.txt" # csv file or txt file with the vocabs to be inserted (one word each line)
NEW_VOCAB = "my-vocab.txt" # path to write out the changes WordPiece voabulary

vocabulary <- read_file(EXISTING_VOCABS) %>% str_split("\n") %>% unlist() %>% {.[1:30000]}

add_vocab <- function(new_vocab, vocabulary) {

  if (!str_detect(paste(vocabulary, collapse = ""), new_vocab)) {

    unused <- str_detect(vocabulary, "unused") 
    unused[2] <- FALSE # this likely indicates how many vocabs are not used
    index_unused <- (1:length(vocabulary))[unused]
    vocabulary[index_unused[1]] <- new_vocab
    vocabulary[index_unused[-1]] <- paste("[unused", 1:(length(index_unused)-1), "]", sep = "")
    vocabulary[2] <- paste("[unused", length(index_unused), "]", sep = "")
    
  }
  
  return(vocabulary)
}

new_vocabs <- read_file(VOCABS_TO_INSERT) %>% str_split("\n") %>% unlist() %>% {.[-length(.)]}
for (i in new_vocabs) vocabulary <- add_vocab(i, vocabulary)

write_file(paste(vocabulary, collapse = "\n"), NEW_VOCAB)
