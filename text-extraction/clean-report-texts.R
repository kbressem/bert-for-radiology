# load packages
library(magrittr)
library(tidyverse)
library(tictoc)

# load rds dump
path_to_rds_dump <- "/path/to/REPORT_TEXT_DUMP.RDS"
TEXT_DUMP <- read_rds(path_to_rds_dump) %>% drop_na() # 33 sec

# identify most frequent strings
freqfunc <- function(x, n) unlist(x) %>% table() %>% sort() %>% tail(n) %>% names()

x <- unlist(TEXT_DUMP$TEXT) 
x <- table(x)
x <- sort(x)
str_to_remove_full_match <- names(tail(x, 100))
str_to_remove_partial_match <- c("Konstanzprüfung", 
                   "RK Import und digitale Archivierung von Fremdaufnahmen im PACS ohne Befunderstellung", 
                   "Demonstration ohne Befunderstellung", 
                   "Befundung erfolgt über eine externe Datenbank.", 
                   "Patient nicht erschienen am", 
                   "Qualitätssicherung", 
                   "Teleradiologische Bildübertragung ohne Befunderstellung", 
                   "Tumorkonferenzbetreuung",
                   "von Station abgesagt",
                   "Demonstration ohne Befunderstellung", 
                   "Import und digitale Archivierung von Fremdaufnahmen",
                   "Patient nicht erschienen am" 
                   )


#remove most frequent strings by full match
#I use a loop, as it allows for better tracking
for (i in str_to_remove_full_match) {
  print(paste("removing: ", i))
  TEXT_DUMP %<>% filter(TEXT != i)
}

# remove strings by partial match
# this is very unelegant tbh. It also takes very long but it works. 
for (i in str_to_remove_partial_match) {
  print(paste("removing: ", i))
  print(nrow(TEXT_DUMP))
  remove = lapply(TEXT_DUMP$TEXT, str_detect, i) %>% unlist
  if (!is.null(remove)) TEXT_DUMP <- TEXT_DUMP[!remove, ]
}

write_rds(TEXT_DUMP, "data/cleaned-text-dump.rds")
write_csv(TEXT_DUMP, "data/cleaned-text-dump.csv")

