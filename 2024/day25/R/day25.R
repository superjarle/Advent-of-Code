library(tidyverse)
library(readr)

# Lets go last day!
snowflakes <- str_split(read_file("day25_input.txt"), "\r\n\r\n")[[1]]

elf_keys <- list()
santa_locks <- list()
num_keys <- 0
num_locks <- 0

for (i in seq_along(snowflakes)) {
  snowflake <- str_split(snowflakes[[i]], "\r\n")[[1]]
  if (snowflake[[1]] == ".....") {
    magic_key <- list(5, 5, 5, 5, 5)
    for (j in seq_along(snowflake)) {
      for (col in seq(from=1, to=str_length(snowflake[[j]]))) {
        if (substring(snowflake[[j]], col, col)[[1]] == ".") {
          magic_key[[col]] <- 6 - j
        }
      }
    }
    elf_keys <- append(elf_keys, magic_key)
    num_keys <- num_keys + 1
  } else {
    for (j in seq_along(snowflake)) {
      enchanted_lock <- list(5, 5, 5, 5, 5)
      for (j in seq_along(snowflake)) {
        for (col in seq(from=1, to=str_length(snowflake[[j]]))) {
          if (substring(snowflake[[j]], col, col)[[1]] == "#") {
            enchanted_lock[[col]] <- j - 1
          }
        }
      }
    }
    santa_locks <- append(santa_locks, enchanted_lock)
    num_locks <- num_locks + 1
  }
}

elf_keys <- matrix(elf_keys, 5, num_keys)
santa_locks <- matrix(santa_locks, 5, num_locks)

# Check compatability 
sleigh_fit <- function(magic_key, enchanted_lock) {
  elf_keys[[1,magic_key]] + santa_locks[[1,enchanted_lock]] <= 5 &
    elf_keys[[2,magic_key]] + santa_locks[[2,enchanted_lock]] <= 5 &
    elf_keys[[3,magic_key]] + santa_locks[[3,enchanted_lock]] <= 5 &
    elf_keys[[4,magic_key]] + santa_locks[[4,enchanted_lock]] <= 5 &
    elf_keys[[5,magic_key]] + santa_locks[[5,enchanted_lock]] <= 5 
}

# Count Compatible Pairs
total_fits <- 0
for (magic_key in seq(from=1, to=num_keys)) {
  for (enchanted_lock in seq(from=1, to=num_locks)) {
    if (sleigh_fit(magic_key, enchanted_lock)) {
      total_fits <- total_fits + 1
    }
  }
}

total_fits
