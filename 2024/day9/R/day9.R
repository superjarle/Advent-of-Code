# Load and map input
input <- readLines("day9_input.txt")
disk_map <- as.numeric(unlist(strsplit(paste0(input, collapse = ""), split = "")))
last_file <- length(disk_map) %/% 2

# Initialize blocks
blocks <- integer()
current_file <- 0
position <- 1

# Make  the initial disk layout
while (current_file < last_file) {
  # Add file blocks
  blocks <- c(blocks, rep(current_file, disk_map[position]))
  
  # Add space blocks (-1 as a placeholder for space)
  blocks <- c(blocks, rep(-1, disk_map[position + 1]))
  
  # Move to the next file
  current_file <- current_file + 1
  position <- position + 2
}

# Add the last file
blocks <- c(blocks, rep(current_file, disk_map[position]))

# Part 1: Sort files to the beginning of the disk
first_disk <- blocks

while (TRUE) {
  space_indices <- which(first_disk == -1)
  file_indices <- which(first_disk != -1)
  
  # Exit if all spaces are sorted at the end
  if (max(file_indices) <= min(space_indices)) break
  
  # Swap the last file block with the first space block
  first_disk[min(space_indices)] <- first_disk[max(file_indices)]
  first_disk[max(file_indices)] <- -1
}

# Replace spaces (-1) with zeros
first_disk[first_disk == -1] <- 0

# Part 2: Optimize file placement to fit files into the smallest available spaces
second_disk <- blocks

unique_files <- rev(setdiff(unique(second_disk), c(-1)))
for (file in unique_files) {
  # Summarize disk state using rle (run-length encoding)
  disk_state <- data.frame(
    block_type = rle(second_disk)$values,
    block_size = rle(second_disk)$lengths
  )
  disk_state$start_index <- cumsum(disk_state$block_size) - disk_state$block_size + 1
  
  # Get the position and size of the current file
  file_position <- min(which(second_disk == file))
  file_size <- disk_state$block_size[disk_state$block_type == file]
  
  # Find the smallest space that can fit the file
  suitable_space_start <- min(disk_state$start_index[
    disk_state$block_type == -1 & disk_state$block_size >= file_size
  ])
  
  # Move the file if the suitable space is before the current position
  if (suitable_space_start < file_position) {
    second_disk[seq(from = suitable_space_start, length.out = file_size)] <- file
    second_disk[seq(from = file_position, length.out = file_size)] <- -1
  }
}

# Replace spaces (-1) with zeros
second_disk[second_disk == -1] <- 0

# Answers
first_checksum <- sum(first_disk * (seq_along(first_disk) - 1))
cat(sprintf("Part 1: %.0f\n", first_checksum)) 
second_checksum <- sum(second_disk * (seq_along(second_disk) - 1))
cat(sprintf("Part 2: %.0f\n", second_checksum)) 