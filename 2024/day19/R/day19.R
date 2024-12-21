
# File with Santa's towel rules
file_name <- 'day19_input.txt'

# Load input data
input_data <- readLines(file_name)
towel_patterns <- strsplit(input_data[1], ", ")[[1]]
mystery_patterns <- input_data[-(1:2)]

# Holiday cache for pattern matching
cache <- collections::dict()

calculate_possibilities <- function(towels, pattern) {
  if (cache$has(pattern)) {
    return(cache$get(pattern))
  }
  
  if (pattern == "") return(1)
  
  possible_count <- 0
  for (towel in towels) {
    if (startsWith(pattern, towel)) {
      possible_count <- possible_count + calculate_possibilities(towels, gsub(paste0("^", towel), "", pattern))
    }
  }
  
  cache$set(pattern, possible_count)
  return(possible_count)
}

# Calculate results for all mystery patterns
results <- sapply(mystery_patterns, function(x) calculate_possibilities(towel_patterns, x))

# Part 1: Count valid patterns
valid_patterns <- sum(results > 0)
cat("Part 1: Number of valid patterns:", valid_patterns, "\n")

# Part 2: Total possible combinations
total_combinations <- sum(results)
cat("Part 2: Total combinations:", total_combinations, "\n")