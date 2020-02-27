# handclean WordPiece Vocabulary
library(tidyverse)
vocab <- read_csv('vocab-bert-1000-handcleaned.txt', col_names = 'token')
# Numbers (like dates), ':', ',', '(' and ')' were removed from the WordPiece vocabulary, leaving duplicated words. 
# " and ' were also removed
# e.g. ['(Serie', 'Serie'] now became ['Serie' 'Serie']
tokens <- vocab %>% select(token) %>% unique() %>% unlist()

# padding to 30 000 tokes inserting [unusedX] tokens 
for (i in 1:(30000-length(tokens))) tokens = c(tokens, paste('[unused', i, ']', sep = ''))
write_csv(data.frame(tokens), 'vocab-bert-handcleaned-30000.txt')
                                        
