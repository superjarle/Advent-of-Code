library(tidyverse)

# Load and parse the input file
input <- readLines("input_day5.txt")

# Split into rules and updates based on the blank line
split_index <- which(input == "")[1]  # Find the blank line separating rules and updates
rules_raw <- input[1:(split_index - 1)]  # Rules section
updates_raw <- input[(split_index + 1):length(input)]  # Updates section

# Parse rules into a tibble
rules <- rules_raw |>
  as_tibble() |>
  separate(value, into = c("page_before", "page_after"), sep = "\\|") |>
  mutate(
    page_before = as.numeric(page_before),
    page_after = as.numeric(page_after)
  ) |>
  group_by(page_before) |>
  summarize(page_after = list(page_after), .groups = "drop")

# Parse updates into a list of numeric vectors
updates <- updates_raw |>
  map(~ as.numeric(str_split(.x, ",")[[1]]))

# Function to check if an update is in the correct order
is_in_correct_order <- function(pages) {
  l <- length(pages)
  for (i in 1:(l - 1)) {
    possible_pages <- rules |>
      filter(page_before == pages[i]) |>
      pull(page_after) |>
      unlist()
    remaining_pages <- pages[(i + 1):l]
    
    if (!all(map_lgl(remaining_pages, ~ .x %in% possible_pages))) {
      return(FALSE)
    }
  }
  return(TRUE)
}

# Function to extract the middle page of a correctly ordered update
get_middle_page <- function(pages) {
  pages[ceiling(length(pages) / 2)]
}

# Part 1: Sum of middle pages of updates already in the correct order
part1_result <- updates |>
  keep(is_in_correct_order) |>
  map_dbl(get_middle_page) |>
  sum()

print(part1_result)

# Function to reorder an update to make it correct
reorder_update <- function(pages) {
  if (is_in_correct_order(pages)) {
    return(pages)
  }
  
  l <- length(pages)
  while (!is_in_correct_order(pages)) {
    for (i in 1:(l - 1)) {
      possible_pages <- rules |>
        filter(page_before == pages[i]) |>
        pull(page_after) |>
        unlist()
      
      for (j in (i + 1):l) {
        if (!pages[j] %in% possible_pages) {
          pages <- c(pages[j], pages[-j])  # Move the out-of-place page to the front
          break
        }
      }
    }
  }
  return(pages)
}

# Part 2: Sum of middle pages of reordered updates
part2_result <- updates |>
  discard(is_in_correct_order) |>
  map(reorder_update) |>
  map_dbl(get_middle_page) |>
  sum()

print(part2_result)
