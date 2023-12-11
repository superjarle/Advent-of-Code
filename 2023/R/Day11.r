library(tidyverse)

cosmic <- readLines("day11.txt")
init <- function(cosmic_data) {

    cosmic_data <- strsplit(cosmic_data, split = "") |> do.call(what = rbind)

    nb_cosmic <- sum(cosmic_data != ".")
    cosmic_data[cosmic_data != "."] <- seq_len(nb_cosmic)

    return(cosmic_data)
}


find_galaxy <- function(nb, cosmic_data) {
  pos <- which(as.matrix(cosmic_data) == nb, arr.ind = TRUE)
  if(length(pos) == 0) return(c(NA, NA))  # Return NA if not found
  c(x = pos[1, 1], y = pos[1, 2])
}


get_all_dist <- function(nb_expansion, cosmic_data) {

    nb_cosmic <- sum(cosmic_data != ".")
    empty_rows <- which(apply(X = cosmic_data,
                              MARGIN = 1,
                              FUN = \(x) sum(x != ".") == 0))
    empty_cols <- which(apply(X = cosmic_data,
                              MARGIN = 2,
                              FUN = \(x) sum(x != ".") == 0))

    data_distance <- vapply(X = seq_len(nb_cosmic),
                            FUN = find_galaxy, cosmic_data,
                            FUN.VALUE = numeric(2))

    length <- 0
    for (gk in seq_len(nb_cosmic - 1) + 1) {
        pos_gk <- data_distance[, gk]
        for (gj in seq_len(gk - 1)) {
            pos_gj <- data_distance[, gj]

            expansion <- (nb_expansion - 1) *
                (sum(empty_rows %in% seq(pos_gk[1], pos_gj[1])) +
                     sum(empty_cols %in% seq(pos_gk[2], pos_gj[2])))

            distance <- abs(pos_gk[1] - pos_gj[1]) +
                abs(pos_gk[2] - pos_gj[2]) +
                expansion

            length <- length + distance
        }
    }
    return(length)
}

solve_part1 <- function(cosmic_data) {
    cosmic_data <- init(cosmic_data)
    return(get_all_dist(nb_expansion = 2, cosmic_data))
}

solve_part2 <- function(cosmic_data) {
    cosmic_data <- init(cosmic_data)
    return(get_all_dist(nb_expansion = 1000000, cosmic_data))
}

solve_part1(cosmic)
solve_part2(cosmic)