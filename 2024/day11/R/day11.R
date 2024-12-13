# Read input data
INPUT_FILE <- 'day11_input.txt'
input_lines <- readLines(INPUT_FILE)
initial_stones <- strsplit(input_lines, " ")[[1]] |> as.numeric()

# Cache for memoization
cache <- collections::dict()

# Recursive function to count stones after blinks
count_stones_after_blinks <- function(stone_value, remaining_blinks) {
  if(remaining_blinks == 0)
    return(1)
  if(cache$has(c(stone_value, remaining_blinks))){
    return(cache$get(c(stone_value, remaining_blinks)))
  }
  
  # Rule 1: Replace stone engraved with 0
  if(stone_value == 0){
    result <- count_stones_after_blinks(1, remaining_blinks - 1)
  } else if(num_digits(stone_value) %% 2 == 0){
    # Rule 2: Split stone if it has an even number of digits
    num_length <- num_digits(stone_value)
    left_part <- stone_value %/% 10^(num_length / 2)
    right_part <- stone_value %% 10^(num_length / 2)
    result <- count_stones_after_blinks(left_part, remaining_blinks - 1) + 
      count_stones_after_blinks(right_part, remaining_blinks - 1)
  } else {
    # Rule 3: Multiply by 2024
    new_stone_value <- stone_value * 2024
    result <- count_stones_after_blinks(new_stone_value, remaining_blinks - 1)
  }
  
  cache$set(c(stone_value, remaining_blinks), result)
  result
}


num_digits <- function(stone_value) floor(log10(stone_value)) + 1

# Solutions
part1 <- sum(sapply(initial_stones, count_stones_after_blinks, remaining_blinks = 25))
print(part1)
part2 <- sum(sapply(initial_stones, count_stones_after_blinks, remaining_blinks = 75))
print(part2)