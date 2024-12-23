# Load input
file_name <- 'day8_input.txt'
num_columns <- nchar(readLines(file_name)[1])
input_matrix <- read.fwf(file_name, widths = rep(1, num_columns), comment.char = "") |> as.matrix()
num_rows <- nrow(input_matrix)
num_cols <- ncol(input_matrix)

# Initialize matrices for antinodes
antinodes_part1 <- matrix(FALSE, num_rows, num_cols)
antinodes_part2 <- matrix(FALSE, num_rows, num_cols)
unique_antennas <- sort(unique(input_matrix[input_matrix != '.']))

# Helper function to check bounds
is_within_bounds <- function(coord) {
  coord[1] >= 1 && coord[1] <= num_rows && coord[2] >= 1 && coord[2] <= num_cols
}

# Main computation
for (antenna in unique_antennas) {
  
  # Get all coordinates of the current antenna
  antenna_positions <- which(input_matrix == antenna, arr.ind = TRUE)
  
  # Skip if only one occurrence
  if (nrow(antenna_positions) < 2) next
  
  # Generate all pair combinations of antenna positions
  position_combinations <- combn(seq_len(nrow(antenna_positions)), 2)
  
  for (i in seq_len(ncol(position_combinations))) {
    pair1 <- antenna_positions[position_combinations[1, i], ]
    pair2 <- antenna_positions[position_combinations[2, i], ]
    distance <- abs(pair1 - pair2)
    
    # Determine direction for antinodes
    left_right <- if (pair1[2] < pair2[2]) 1 else -1
    up_down <- if (pair1[1] < pair2[1]) 1 else -1
    
    # Antinode for pair1
    current_antinode <- pair1 - c(up_down * distance[1], left_right * distance[2])
    if (is_within_bounds(current_antinode)) {
      antinodes_part1[current_antinode[1], current_antinode[2]] <- TRUE
    }
    while (is_within_bounds(current_antinode)) {
      antinodes_part2[current_antinode[1], current_antinode[2]] <- TRUE
      current_antinode <- current_antinode - c(up_down * distance[1], left_right * distance[2])
    }
    
    # Antinode for pair2
    current_antinode <- pair2 + c(up_down * distance[1], left_right * distance[2])
    if (is_within_bounds(current_antinode)) {
      antinodes_part1[current_antinode[1], current_antinode[2]] <- TRUE
    }
    while (is_within_bounds(current_antinode)) {
      antinodes_part2[current_antinode[1], current_antinode[2]] <- TRUE
      current_antinode <- current_antinode + c(up_down * distance[1], left_right * distance[2])
    }
    
    # Ensure original antenna positions are marked
    antinodes_part2[pair1[1], pair1[2]] <- TRUE
    antinodes_part2[pair2[1], pair2[2]] <- TRUE
  }
}

# Output results
sum(antinodes_part1)
sum(antinodes_part2)
