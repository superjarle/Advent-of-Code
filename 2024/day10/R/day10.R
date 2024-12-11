library(purrr)
library(dplyr)

# Load input file
load_input <- function(file_name) {
  lines <- readLines(file_name)
  input_matrix <- do.call(rbind, strsplit(lines, "")) |> apply(2, as.integer)
  list(input = input_matrix, rows = nrow(input_matrix), cols = ncol(input_matrix))
}

# Traverse height levels and calculate scores and ratings
calculate_scores_and_ratings <- function(input_matrix, rows, cols) {
  reachable_positions <- vector("list", rows * cols)
  trail_count <- matrix(0, nrow = rows, ncol = cols)
  
  total_score <- 0
  total_rating <- 0
  
  for (height in 9:0) {
    for (row in 1:rows) {
      for (col in 1:cols) {
        if (input_matrix[row, col] != height) next
        
        index <- (row - 1) * cols + col
        if (height == 9) {
          reachable_positions[[index]] <- list(c(row, col))
          trail_count[row, col] <- 1
        } else {
          neighbors <- list(
            c(row + 1, col), c(row - 1, col),
            c(row, col + 1), c(row, col - 1)
          )
          
          reachable <- list()
          count <- 0
          
          for (neighbor in neighbors) {
            r <- neighbor[1]
            c <- neighbor[2]
            
            if (r >= 1 && r <= rows && c >= 1 && c <= cols && input_matrix[r, c] == height + 1) {
              neighbor_index <- (r - 1) * cols + c
              reachable <- unique(c(reachable, reachable_positions[[neighbor_index]]))
              count <- count + trail_count[r, c]
            }
          }
          
          reachable_positions[[index]] <- reachable
          trail_count[row, col] <- count
        }
        
        if (height == 0) {
          total_score <- total_score + length(reachable_positions[[index]])
          total_rating <- total_rating + trail_count[row, col]
        }
      }
    }
  }
  
  list(total_score = total_score, total_rating = total_rating)
}

# Main function
main <- function(file_name) {
  input_data <- load_input(file_name)
  input_matrix <- input_data$input
  rows <- input_data$rows
  cols <- input_data$cols
  
  results <- calculate_scores_and_ratings(input_matrix, rows, cols)
  results
}

# Run the solution
file_name <- "day10_input.txt"
results <- main(file_name)
cat("Part 1 (Total Score):", results$total_score, "\n")
cat("Part 2 (Total Rating):", results$total_rating, "\n")