# Function to calculate the sum of sequences satisfying a "safe" condition
safe_sequence_count <- function(file_path = "day2_input.txt") {
  # Read the input file line by line
  input_lines <- readLines(file_path)
  
  # Convert each line into a list of integers
  sequences <- sapply(strsplit(input_lines, " "), as.integer, simplify = FALSE)
  
  # Define the "safe" condition for a sequence
  is_safe <- function(sequence) {
    # Compute differences between adjacent elements
    differences <- diff(sequence)
    # Check if all differences are within a valid range
    all(differences > 0 & differences < 4) || all(differences < 0 & differences > -4)
  }
  
  # Apply the "safe" condition to each sequence and sum up the results
  safe_count <- sum(sapply(sequences, is_safe))
  
  return(safe_count)
}

#' Function to calculate the sum of sequences where any sub-sequence is "safe"
#' @param file_path Path to the input file
#' @export
safe_subsequence_count <- function(file_path = "day2_input.txt") {
  # Read the input file line by line
  input_lines <- readLines(file_path)
  
  # Convert each line into a list of integers
  sequences <- sapply(strsplit(input_lines, " "), as.integer, simplify = FALSE)
  
  # Define the "safe" condition for sub-sequences
  is_any_subsequence_safe <- function(sequence) {
    # Iterate through each element in the sequence
    for (index in seq_along(sequence)) {
      # Exclude the current element to create a sub-sequence
      subsequence <- sequence[-index]
      
      # Compute differences for the sub-sequence
      differences <- diff(subsequence)
      
      # Check if the sub-sequence satisfies the "safe" condition
      if (all(differences > 0 & differences < 4) || all(differences < 0 & differences > -4)) {
        return(TRUE)
      }
    }
    return(FALSE)
  }
  
  # Apply the "safe" condition to each sequence and sum up the results
  safe_count <- sum(sapply(sequences, is_any_subsequence_safe))
  
  return(safe_count)
}

# Call the functions
safe_sequence_result <- safe_sequence_count()
safe_subsequence_result <- safe_subsequence_count()

# Print results
print(safe_sequence_result)
print(safe_subsequence_result)
