# Part One ----------------------------------------------------------------

parse_dish <- function(input) {
  dish <- input |>
    lapply(\(line) strsplit(line, "") |> unlist()) |>
    unlist() |>
    matrix(nrow = length(input)) |>
    t()
}

tilt_north <- function(dish, dir, load) {
  total_load <- numeric()
  
  for (col in 1:ncol(dish)) {
    # For each O
    # Move it upwards if there is a dot above
    # Store highest possible point
    vec <- dish[, col]
    available_highest <- 1
    
    for (row in 1:nrow(dish)) {
      val <- vec[[row]]
      
      if (val == "O") {
        # Rock's current position as empty
        vec[[row]] <- "."
        # Move the rock up
        vec[[available_highest]] <- "O"
        
        load <- nrow(dish) - available_highest + 1
        total_load <- c(total_load, load)
        
        available_highest <- available_highest + 1
      }
      
      if (val == "#") {
        available_highest <- row + 1
      }
      # if (val == ".") next
    }
    dish[, col] <- vec
  }
  
  dish
}

get_load <- function(dish) {
  total_load <- numeric()
  for (col in 1:ncol(dish)) {
    for (row in 1:nrow(dish)) {
      if (dish[row, col] == "O") {
        load <- nrow(dish) - row + 1
        total_load <- c(total_load, load)
      }
    }
  }
  
  total_load <- sum(total_load)
}

solve_day_14_p1 <- function(input) {
  dish <- parse_dish(input)
  dish <- tilt_north(dish)
  
  load <- get_load(dish)
  
  print(load)
}

# Part Two ----------------------------------------------------------------

rotate_dish_clockwise <- function(dish) {
  return(apply(dish, 2, rev) |>  t())
}

# Defaults of 5 set by eyeballing
# If we find a sequence repeated 5 times, we assume that's the one.
# We also assume the sequence take at least 5 cycles.
# Neither of those are necessarily true, but worked for the/my input
find_repeating_sequence <- function(vec, min_length = 5, min_reps = 5) {
  # min_reps is the minimum number of times a sequence must repeat
  # for us to consider it a repeating sequence
  
  # min_length is to skip checking very small lengths
  
  vec_length <- length(vec)
  max_length <- vec_length / min_reps
  
  for (seq_length in min_length:max_length) {
    # Generate a sequence from the end of the vector
    seq <- vec[vec_length:(vec_length - seq_length + 1)]
    
    # Repeat the sequence for the length of repetitions we want to check
    rep_seq <- rep(seq, min_reps)
    
    # Find the actual sequence of the same length
    act_seq <- vec[vec_length:(vec_length - min_reps * seq_length + 1)]
    
    # If the repeated sequence is equal to the actual sequence
    # Then we've
    rep_found <- prod(rep_seq == act_seq) == 1
    
    if (rep_found) {
      return(list(start = vec_length - seq_length, length = seq_length))
    }
  }
}

solve_day_14_p2 <- function(input) {
  loads <- numeric()
  moving_dish <- parse_dish(input)
  for (loop in 1:500) {
    for (dir in 1:4) {
      moving_dish <- tilt_north(moving_dish, dir, load)
      moving_dish <- rotate_dish_clockwise(moving_dish)
      if (dir == 4) {
        loads <- c(loads, get_load(moving_dish))
      }
    }
  }
  
  # We need to find a repetition of cycles and a start position of that
  # loads[[rep_start + (n - rep_start %% rep_length]]
  # Where n is the number of cycles (1,000,000,000)
  rep_seq <- find_repeating_sequence(loads)
  
  rep_start <- rep_seq$start
  rep_length <- rep_seq$length
  
  n = 10000000000
  
  result <-  loads[[rep_start + (n - rep_start) %% rep_length]]
  
  print(result)
}