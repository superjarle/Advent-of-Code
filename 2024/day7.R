library(gtools)

# Load input
file_name <- 'day7_input.txt'
input_data <- readLines(file_name) |> strsplit(": ")
calibrations <- sapply(input_data, \(x) as.numeric(x[1]))
numbers_list <- lapply(input_data, \(x) as.numeric(strsplit(x[2], " ")[[1]]))

# Combine two numbers without converting to strings
combine_numbers <- function(x, y) {
  x * 10^(floor(log10(y)) + 1) + y
}

# Calculate the number of digits in a number
num_digits <- function(num) {
  floor(log10(num)) + 1
}

# Check if `a` ends with `b`
ends_with <- function(a, b) {
  (a %% 10^num_digits(b)) == b
}

# Remove digits of `b` from the end of `a`
remove_digits <- function(a, b) {
  a %/% (10^num_digits(b))
}

# Recursively check if a valid calculation exists
check_validity_recursive <- function(target, numbers, allow_concatenation = FALSE) {
  n <- length(numbers)
  
  # Base case: single number
  if (n == 1) {
    return(target == numbers[1])
  }
  
  # Multiplication
  if (target %% numbers[n] == 0 && 
      check_validity_recursive(target / numbers[n], numbers[-n], allow_concatenation)) {
    return(TRUE)
  }
  
  # Concatenation (only if allowed)
  if (allow_concatenation && ends_with(target, numbers[n]) && 
      check_validity_recursive(remove_digits(target, numbers[n]), numbers[-n], allow_concatenation)) {
    return(TRUE)
  }
  
  # Addition
  if (check_validity_recursive(target - numbers[n], numbers[-n], allow_concatenation)) {
    return(TRUE)
  }
  
  return(FALSE)
}

# Compute results
part1_sum <- 0
part2_sum <- 0

for (i in seq_along(calibrations)) {
  calibration <- calibrations[i]
  numbers <- numbers_list[[i]]
  
  # Check Part 1 (multiplication and addition only)
  if (check_validity_recursive(calibration, numbers, allow_concatenation = FALSE)) {
    part1_sum <- part1_sum + calibration
    part2_sum <- part2_sum + calibration
  } else {
    # Check Part 2 (allow concatenation)
    if (check_validity_recursive(calibration, numbers, allow_concatenation = TRUE)) {
      part2_sum <- part2_sum + calibration
    }
  }
}

# Output results
part1_sum
part2_sum
