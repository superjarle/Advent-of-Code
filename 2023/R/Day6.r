library(readr)
library(dplyr)
library(purrr)
library(stringr)

# Leser inn
filsti <- "day6.txt"  
linjer <- read_lines(filsti)

# Parsing 
tid_multi <- str_extract_all(linjer[1], "\\d+")[[1]] %>% as.numeric()
distace_multi <- str_extract_all(linjer[2], "\\d+")[[1]] %>% as.numeric()

# Regne ut for hvert race
calc_multi <- function(time, record_distance) {
  speeds <- 1:(time - 1)
  travel_times <- time - speeds
  distances_travelled <- speeds * travel_times
  sum(distances_travelled > record_distance)
}

# Hvor mange m??ter ?? vinne per race
ways_per_race <- map2_dbl(tid_multi, distace_multi, calc_multi)
total_q1 <- prod(ways_per_race)

# Hver linje et tall
tid_single <- as.numeric(str_replace_all(lines[1], "\\D", ""))
distanse_single <- as.numeric(str_replace_all(lines[2], "\\D", ""))

# Vinne et single race 
calc_single <- function(time, record_distance) {
  vinne <- 0
  for (button_hold_time in 1:(time - 1)) {
    travel_time <- time - button_hold_time
    distance_travelled <- button_hold_time * travel_time
    if (distance_travelled > record_distance) {
      vinne <- vinne + 1
    }
  }
  return(vinne)
}

# Single race
total_q2 <- calc_single(tid_single, distanse_single)

# Output
cat("Svaret for flere race (q1) er::", total_ways_to_win_multi, "\n")
cat("antall mulige veier man vinner er:", paste(ways_per_race, collapse = ", "), "\n")
cat("Svaret for et race (q2) er:", total_q2, "\n")
