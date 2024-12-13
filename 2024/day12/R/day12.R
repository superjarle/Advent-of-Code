# Input file
INPUT_FILE <- 'day12_input.txt'
W <- nchar(readLines(INPUT_FILE)[1])
grid <- read.fwf(INPUT_FILE, widths = rep(1, W)) |> as.matrix()
rows <- nrow(grid)
cols <- W

# Initialize matrices
region_touching <- matrix(-1, rows, cols)
visited <- matrix(FALSE, rows, cols)

# Unique region values
region_values <- sort(unique(as.vector(grid)))

# Function to find neighbors
find_neighbors <- function(current_position) {
  list(
    c(current_position[1] - 1L, current_position[2]),      # Up
    c(current_position[1], current_position[2] + 1L),      # Right
    c(current_position[1] + 1L, current_position[2]),      # Down
    c(current_position[1], current_position[2] - 1L)       # Left
  )
}

# Function to compute complex perimeter conditions
compute_perimeter_complex <- function(coords) {
  if (nrow(coords) < 3) return(4)
  
  coords_complex <- complex(real = coords[, 1], imaginary = coords[, 2])
  directions <- list(-1 + 0i, 1i, 1 + 0i, -1i)
  total_sides <- 0
  
  for (pt in coords_complex) {
    for (i in 1:4) {
      d1 <- directions[[i]]
      d2 <- directions[[i %% 4 + 1]]
      n1 <- pt + d1
      n2 <- pt + d2
      n3 <- pt + d1 + d2
      
      if (n1 %in% coords_complex && n2 %in% coords_complex && !n3 %in% coords_complex) {
        total_sides <- total_sides + 1
      } else if (!n1 %in% coords_complex && !n2 %in% coords_complex) {
        total_sides <- total_sides + 1
      }
    }
  }
  
  total_sides
}

# Function to calculate area and perimeter for a single region
calculate_region_properties <- function(region_char) {
  region_positions <- which(grid == region_char, arr.ind = TRUE)
  position_list <- apply(region_positions, 1, \(x) list(x)[[1]], simplify = FALSE)
  seen <- collections::dict(keys = position_list, items = rep(FALSE, length(position_list)))
  
  total_area_perimeter1 <- 0
  total_area_perimeter2 <- 0
  
  for (i in 1:nrow(region_positions)) {
    current_position <- region_positions[i, ]
    
    if (seen$get(current_position)) next
    seen$set(current_position, TRUE)
    region_touching[] <- -1
    
    # Flood fill to find the entire region
    queue <- collections::queue()
    queue$push(current_position)
    
    while (queue$size() > 0) {
      current <- queue$pop()
      region_touching[current[1], current[2]] <- 0
      
      for (neighbor in find_neighbors(current)) {
        if (neighbor[1] < 1 | neighbor[1] > rows | neighbor[2] < 1 | neighbor[2] > cols) next
        if (grid[neighbor[1], neighbor[2]] != region_char) next
        
        region_touching[current[1], current[2]] <- region_touching[current[1], current[2]] + 1
        
        if (seen$get(neighbor)) next
        
        queue$push(neighbor)
        seen$set(neighbor, TRUE)
      }
    }
    
    # Calculate area and perimeter for the region
    perimeter1 <- sum(4 - region_touching[region_touching != -1])
    area <- sum(region_touching != -1)
    total_area_perimeter1 <- total_area_perimeter1 + area * perimeter1
    
    indices <- which(region_touching != -1, arr.ind = TRUE)
    perimeter2 <- compute_perimeter_complex(indices)
    total_area_perimeter2 <- total_area_perimeter2 + area * perimeter2
  }
  
  c(total_area_perimeter1, total_area_perimeter2)
}

# Initialize results
part1 <- 0
part2 <- 0

# Process each region
for (region_char in region_values) {
  results <- calculate_region_properties(region_char)
  part1 <- part1 + results[1]
  part2 <- part2 + results[2]
}

# Solutions
part1
part2
