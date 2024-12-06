# Read the input file
map <- readLines("day06_input.txt")

# Initialize the map
initialize_map <- function(data_map) {
  map <- strsplit(data_map, split = "", fixed = TRUE) |>
    do.call(what = rbind)
  
  map[map == "^"] <- 0L
  map[map == "."] <- 0L
  map[map == "#"] <- -1L
  map <- rbind(-2L, map, -2L)
  map <- cbind(-2L, map, -2L)
  map <- as.numeric(map)
  dim(map) <- c(length(data_map) + 2L, nchar(data_map[1]) + 2L)
  
  return(map)
}

# Get the initial position of the guard
initial_position <- function(data_map) {
  map <- strsplit(data_map, split = "", fixed = TRUE) |>
    do.call(what = rbind)
  pos <- which(map == "^", arr.ind = TRUE)
  return(pos + 1L) # Offset for padding
}

# Move the guard
move_position <- function(position, direction, steps = 1L) {
  offsets <- switch(direction,
                    "up" = c(-1L, 0L),
                    "down" = c(1L, 0L),
                    "left" = c(0L, -1L),
                    "right" = c(0L, 1L)
  )
  next_pos <- position + steps * offsets
  return(next_pos)
}

# Browse the map
browse_map <- function(map, start) {
  directions <- c("up", "right", "down", "left")
  pos <- start
  dir <- 1 # Index for `directions`
  visited <- matrix(0, nrow = nrow(map), ncol = ncol(map))
  
  while (TRUE) {
    next_pos <- move_position(pos, directions[dir])
    if (map[next_pos[1], next_pos[2]] == -2L) {
      return(list(visited, success = TRUE))
    } else if (map[next_pos[1], next_pos[2]] == -1L) {
      dir <- dir %% 4 + 1 # Turn right
    } else {
      visited[next_pos[1], next_pos[2]] <- 1
      pos <- next_pos
    }
  }
}

# Part 1 
solve_day06_part1 <- function(data_map) {
  start <- initial_position(data_map)
  map <- initialize_map(data_map)
  visited <- browse_map(map, start)[[1]]
  return(sum(visited > 0))
}

# Part 2 takes forever
solve_day06_part2 <- function(data_map) {
  start <- initial_position(data_map)
  map <- initialize_map(data_map)
  base_map <- browse_map(map, start)[[1]]
  
  positions <- which(base_map > 0, arr.ind = TRUE)
  nb_loop <- 0
  
  for (pos in seq_len(nrow(positions))) {
    temp_map <- map
    temp_map[positions[pos, 1], positions[pos, 2]] <- -1L
    output <- browse_map(temp_map, start)
    if (!output$success) nb_loop <- nb_loop + 1
  }
  
  return(nb_loop)
}

# Solution
## Part 1
cat("Part 1:", solve_day06_part1(map), "\n")

## Part 2
cat("Part 2:", solve_day06_part2(map), "\n")
