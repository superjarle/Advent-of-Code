library(duckdb)

# File with Santa's rocky paths
file_name <- 'day18_input.txt'

# Load input and adjust indices for R
input_data <- strsplit(readLines(file_name), ",") |> lapply(\(x) as.numeric(x) + 1)

# Santa's movement directions
directions <- list(
  c(-1, 0),  # top
  c(0, 1),   # right
  c(1, 0),   # down
  c(0, -1)   # left
)

rows <- 71
cols <- 71

# Create the grid
generate_grid <- function(input, rows, cols, steps) {
  grid <- matrix(".", rows, cols)
  for (rock in input[1:steps]) {
    grid[rock[2], rock[1]] <- "#"
  }
  grid
}

# Find shortest path
calculate_shortest_path <- function(grid, rows, cols) {
  start <- c(1, 1)
  end <- c(rows, cols)
  
  queue <- collections::queue(list(c(start, 0)))
  visited <- matrix(FALSE, rows, cols)
  
  while (queue$size() > 0) {
    current <- queue$pop()
    position <- current[1:2]
    distance <- current[3]
    
    if (all(position == end)) {
      return(list(distance, TRUE))
    }
    
    if (visited[position[1], position[2]]) next
    visited[position[1], position[2]] <- TRUE
    
    for (dir in directions) {
      next_position <- position + dir
      
      if (
        next_position[1] < 1 || next_position[1] > rows ||
        next_position[2] < 1 || next_position[2] > cols ||
        grid[next_position[1], next_position[2]] == "#"
      ) next
      
      queue$push(c(next_position, distance + 1))
    }
  }
  
  list(Inf, FALSE)
}

# Part 2: Binary search with DuckDB
path_exists_at_step <- function(step) {
  grid <- generate_grid(input_data, rows, cols, step)
  calculate_shortest_path(grid, rows, cols)[[2]]
}

binary_search_steps <- function(low, high) {
  if (low > high) return(-1)
  
  mid <- (low + high) %/% 2
  
  mid_result <- path_exists_at_step(mid)
  low_result <- path_exists_at_step(low)
  
  if (low_result && !mid_result) {
    return(binary_search_steps(low, mid - 1))
  } else if (low_result && mid_result) {
    return(binary_search_steps(mid + 1, high))
  } else {
    return(low)
  }
}

# Optimized query using DuckDB
duckdb_query <- function(input_data) {
  con <- duckdb::dbConnect(duckdb::duckdb(), dbdir = "")
  duck_data <- do.call(rbind, input_data)
  colnames(duck_data) <- c("x", "y")
  duck_tbl <- as.data.frame(duck_data)
  
  result <- duckdb::duckdb_query(con, paste0(
    "SELECT step, COUNT(*) AS valid_paths FROM (",
    "SELECT step, CASE WHEN x >= 1 AND x <= ", rows, 
    " AND y >= 1 AND y <= ", cols, " THEN 1 ELSE "0" END ")
    "), returns valid mathig dup position"
  )
  