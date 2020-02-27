library(lubridate)
library(tidyverse)
library(magrittr)

#################################
#                               #
#     run time ~ 3 days         #
#                               #
#################################

# set path, import table ----
REPORTS <- read_rds(paste("~/REPORT_TEXT_DUMP.RDS", sep = ""))
# a very large table with two collumns: 
# FILE_ADDRESS_TEXT_REPORT --> Name of the plain text file with path
# TEXT --> NA for default, report Texts will be placed here


# define variables for monitoring ----
STEPS = 10000
N_TO_EXTRACT = sum(is.na(REPORTS$TEXT))
SAVING_STEPS = (1:round(N_TO_EXTRACT/STEPS))*STEPS + nrow(REPORTS)-N_TO_EXTRACT
# MESSAGE_STEPS = (1:round(N_TO_EXTRACT/(STEPS*10)))*(STEPS*10) + nrow(REPORTS)-N_TO_EXTRACT # uncomment if frequent status reports are desired
START_TIME <- as.numeric(Sys.time())
START = Sys.time()
EST_TIME = 0
TRYS = 0
LAST_SAVE = "NA"
start_iter = sum(!is.na(REPORTS$TEXT))

# start the loop  ----
# loops might be slower and a lot more code than a solution using purrr::map (one line of code) but it allows for better logging. 

  for (i in 1:nrow(REPORTS)) {
    
    if (is.na(REPORTS$TEXT[i])) {
      
    file_adress <- REPORTS$FILE_ADDRESS_TEXT_REPORT[i]  
      
      file <- try(read_file(file_adress)) 
      
      if (class(file) == "try-error") {TRYS = TRYS + 1} else {
        file %<>% str_replace_all("\n", " ") %>% str_replace_all("\r", " ") %>% str_squish()
        REPORTS$TEXT[i] = file
        }
  
      if (i %in% SAVING_STEPS) {
        
        LAST_SAVE <- paste("Iteration:", i, "at:", Sys.time())
        
        print("Saving")
        
        write_csv(REPORTS, "~data/REPORT_TEXT_DUMP.csv")
        write_rds(REPORTS, "~data/REPORT_TEXT_DUMP.RDS")
        
        print("Done")  
      }
  
      # if (i %in% MESSAGE_STEPS) message_me(status_report, parse_mode = 'Markdown') # message_me = custom wrapper for telegram-bot

      if (i %% 100 == 0 ) {
        
        PASSED_TIME <- round(as.numeric(Sys.time()) - START_TIME)
        iterations_passed <- i - start_iter
        EST_TIME <- (PASSED_TIME/iterations_passed) * sum(is.na(REPORTS$TEXT))
        
        status_report <- paste("*Status Update* \n\n",
                               "Current time: ", Sys.time(),"\n",
                               "Start time: ", START, "\n",
                               "Passed time: ", seconds_to_period(PASSED_TIME),"\n",  
                               "Try-erros: ", TRYS, "\n",
                               "Reports extracted: ", sum(!is.na(REPORTS$TEXT)), "\n", 
                               "Reports to extract: ", sum(is.na(REPORTS$TEXT)), "\n", 
                               "Last save: ", LAST_SAVE, "\n",
                               "Est. remaining time: ", seconds_to_period(EST_TIME))  
        cat("\014")  # flushes console
        cat(status_report)
        write_file(status_report, "data/status_report.md")
      
      }
    
    }
  }

