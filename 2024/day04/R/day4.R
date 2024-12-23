library(tidyverse)

# read the puzzle into a matrix
puzzle <- do.call(rbind, read_lines("day4_input.txt") |> str_split(""))

# count occurrences of XMAS both forward and backwards
xmas_count <- function(vec) {
  temp <- paste0(vec, collapse = "")
  sum(str_count(temp, "XMAS") + str_count(temp, "SAMX"))
}

# get every diagonal of "m" and convert 
get_diagonals <- function(m) {
  n <- nrow(m)
  diagonals <- list()
  for (d in -(n - 3):(n - 3)) {
    diagonals[[as.character(d)]] <- paste0(m[row(m) - col(m) == d], collapse = "")
    diagonals[[paste0("reversed_", as.character(d))]] <- paste0(m[row(m) + col(m) == (n - 1 + d)], collapse = "")
  }
  
  diagonals
}

# count XMAS (and SAMX) across rows, columns, and diagonals
apply(puzzle, 1, xmas_count) |>
  sum() +
  apply(puzzle, 2, xmas_count) |>
  sum() +
  get_diagonals(puzzle) |>
  map(xmas_count) |>
  unlist() |>
  sum()

# check vectors
vector_check <- function(vec) {
  paste(vec, collapse = "") %in% c("MAS", "SAM")
}

# check the submatrices as well
check_submatrice <- function(m) {
  vector_check(diag(m)) && vector_check(diag(m[nrow(m):1, ]))
}

solution <- 0
for (i in 1:(nrow(puzzle) - 2)) {
  for (j in 1:(ncol(puzzle) - 2)) {
    solution <- solution + check_submatrice(puzzle[i:(i + 2), j:(j + 2)])
  }
}
solution