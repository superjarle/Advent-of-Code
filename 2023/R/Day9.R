library(tidyverse)

# Func to generate diffs in sequences
diff_sequences <- function(history) {
  sequences <- list(history)
  while (length(unique(sequences[[length(sequences)]])) > 1) {
    new_sequence <- diff(sequences[[length(sequences)]])
    sequences <- append(sequences, list(new_sequence))
  }
  return(sequences)
}

# Function to extrapolate the next or previous value
extrapolate_value <- function(history, direction = "next") {
  sequences <- diff_sequences(history)
  if (direction == "previous") {
    sequences <- lapply(sequences, rev)
  }
  
  for (i in length(sequences):2) {
    sequences[[i - 1]] <- c(sequences[[i - 1]], tail(sequences[[i - 1]], n=1) + tail(sequences[[i]], n=1))
  }
  
  if (direction == "next") {
    return(tail(sequences[[1]], n=1))
  } else {
    return(head(sequences[[1]], n=1))
  }
}

# Function to load data and calculate the sum of extrapolated values
calculate_sum <- function(file_path, direction = "next") {
  histories <- read_lines(file_path) %>% 
    map(~str_split(.x, " ") %>% unlist() %>% as.numeric())
  
  sum_values <- map_dbl(histories, ~extrapolate_value(.x, direction))
  return(sum(sum_values))
}

# Load the data and calculate the sums for both parts
file_path <- "day9.txt"
sum_next_values <- calculate_sum(file_path, "next")
sum_previous_values <- calculate_sum(file_path, "previous")

print(paste("Solution to part 1 is:", sum_next_values))
print(paste("Solution to part 2 is:", sum_previous_values))
