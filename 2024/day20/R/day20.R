library(duckdb)
library(dbplyr)

# Festive file loading
file_name <- 'day20_input.txt'

grid_width <- nchar(readLines(file_name, n = 1))
input_grid <- read.fwf(file_name, widths = rep(1, grid_width), comment.char = "") |> as.matrix()
rows <- nrow(input_grid)
cols <- ncol(input_grid)

distances <- matrix(Inf, rows, cols)

# Santa's directions
movement_directions <- list(
  c(-1, 0),  # top
  c(0, 1),   # right
  c(1, 0),   # down
  c(0, -1)   # left
)

start_position <- unname(which(input_grid == "S", arr.ind = TRUE)[1,])
end_position <- unname(which(input_grid == "E", arr.ind = TRUE)[1,])

# Distance calculation function
generate_distances <- function(grid) {
  distance_matrix <- matrix(Inf, rows, cols)
  distance_matrix[start_position[1], start_position[2]] <- 0
  
  queue <- collections::Queue(list(c(start_position)))
  visited_nodes <- collections::dict()
  
  while (queue$size() > 0) {
    current_position <- queue$pop()
    
    for (direction in movement_directions) {
      next_position <- current_position + direction
      
      if (
        next_position[1] < 1 || next_position[1] > rows ||
        next_position[2] < 1 || next_position[2] > cols ||
        grid[next_position[1], next_position[2]] == "#"
      ) next
      
      if (is.infinite(distance_matrix[next_position[1], next_position[2]])) {
        distance_matrix[next_position[1], next_position[2]] <- distance_matrix[current_position[1], current_position[2]] + 1
        queue$push(next_position)
      }
    }
  }
  distance_matrix
}

original_distances <- generate_distances(input_grid)
reachable_positions <- which(!is.infinite(original_distances), arr.ind = TRUE)

# Memory-friendly computation with DuckDB
con <- duckdb::dbConnect(duckdb::duckdb())
dbWriteTable(con, "grid_data", reachable_positions)

computed_cheats <- tbl(con, "grid_data") |> 
  dplyr::cross_join(tbl(con, "grid_data")) |> 
  dplyr::mutate(
    apart = abs(row.x - row.y) + abs(col.x - col.y),
    saved_time = dist.y - dist.x - apart
  ) |> 
  dplyr::filter(apart > 0) |>  # remove same point combinations
  dplyr::select(apart, saved_time)

# Part 1: Festive two-step cheats
part_1_cheats <- computed_cheats |> 
  dplyr::filter(apart == 2, saved_time >= 100) |> 
  count()

# Part 2: Holiday expansion with up to 20 steps
part_2_cheats <- computed_cheats |> 
  dplyr::filter(apart <= 20, saved_time >= 100) |> 
  count()

print(part_1_cheats)
print(part_2_cheats)
