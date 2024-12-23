# Function to calculate the sum of absolute differences between two sorted vectors
sum_abs_differences <- function(file_path = "day1_input.txt") {
  # Read the input data with appropriate column names
  input_data <- read.table(file_path, col.names = c("x", "y"))
  
  # Sort the columns
  sorted_x <- sort(input_data$x)
  sorted_y <- sort(input_data$y)
  
  # Calculate the sum of absolute differences
  result <- sum(abs(sorted_y - sorted_x))
  
  return(result)
}

#' Function to calculate the weighted sum of occurrences
#' @param file_path Path to the input file
#' @export
weighted_sum_occurrences <- function(file_path = "day1_input.txt") {
  # Read the input data with appropriate column names
  input_data <- read.table(file_path, col.names = c("x", "y"))
  
  # Extract the x and y columns
  values <- input_data$x
  occurrences <- input_data$y
  
  # Initialize accumulator
  total_sum <- 0
  
  # Iterate through unique values in 'x' and compute weighted sum
  for (value in unique(values)) {
    total_sum <- total_sum + value * sum(occurrences == value)
  }
  
  return(total_sum)
}

# Call the functions
sum_abs_differences_result <- sum_abs_differences()
weighted_sum_occurrences_result <- weighted_sum_occurrences()

# Print results
print(sum_abs_differences_result)
print(weighted_sum_occurrences_result)
