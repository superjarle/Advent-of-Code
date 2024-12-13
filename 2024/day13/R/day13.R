library(stringr)

start_time <- Sys.time()

# input and process
input_file <- "day13_input.txt"
lines <- trimws(readLines(input_file))
data_blocks <- strsplit(paste(readLines(input_file), collapse = "\n"), "\n\n")[[1]]
data_blocks <- lapply(data_blocks, function(block) strsplit(block, "\n")[[1]])

# Function to solve those equations
solve_equations <- function(coefficients_x, coefficients_y) {
  constant_diff <- coefficients_x[3] * coefficients_y[1] - coefficients_y[3] * coefficients_x[1]
  coefficient_diff <- coefficients_x[2] * coefficients_y[1] - coefficients_y[2] * coefficients_x[1]
  if (is.na(coefficient_diff) || coefficient_diff == 0 || constant_diff %% coefficient_diff != 0) {
    return(NULL)
  }
  b <- constant_diff %/% coefficient_diff
  
  # Solve for 'a'
  if (is.na(coefficients_x[3]) || is.na(b) || (coefficients_x[3] - b * coefficients_x[2]) %% coefficients_x[1] != 0) {
    return(NULL)
  }
  a <- (coefficients_x[3] - b * coefficients_x[2]) %/% coefficients_x[1]
  
  if (a >= 0 && b >= 0) {
    return(c(a, b))
  }
  return(NULL)
}

# Initialize results
part1_result <- 0
part2_result <- 0

# Process data blocks
for (block in data_blocks) {
  coefficients_x <- numeric(3)
  coefficients_y <- numeric(3)
  
  # Parsing the coefficients
  for (i in seq_len(3)) {
    equation <- strsplit(block[i], ": ")[[1]][2]
    terms <- strsplit(equation, ", ")[[1]]
    coefficients_x[i] <- suppressWarnings(as.integer(str_extract(terms[1], "[0-9-]+")))
    coefficients_y[i] <- suppressWarnings(as.integer(str_extract(terms[2], "[0-9-]+")))
  }
  
  if (any(is.na(coefficients_x)) || any(is.na(coefficients_y))) {
    next
  }
  
  # Solving part 1
  solution <- solve_equations(coefficients_x, coefficients_y)
  if (!is.null(solution)) {
    part1_result <- part1_result + 3 * solution[1] + solution[2]
  }
  
  # Adjusting for part 2 and solving
  coefficients_x[3] <- coefficients_x[3] + 10^13
  coefficients_y[3] <- coefficients_y[3] + 10^13
  solution <- solve_equations(coefficients_x, coefficients_y)
  if (!is.null(solution)) {
    part2_result <- part2_result + 3 * solution[1] + solution[2]
  }
}

# Printing the output
cat(sprintf("Part 1: %d  (%.3fs)\n", part1_result, as.numeric(difftime(Sys.time(), start_time, units = "secs"))))
cat(sprintf("Part 2: %.0f  (%.3fs)\n", part2_result, as.numeric(difftime(Sys.time(), start_time, units = "secs"))))
