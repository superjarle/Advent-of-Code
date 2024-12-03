#' @rdname day03
#' @export

mul <- function(x, y) x*y 

day03a <- function(x) {
  x <- readLines("day3_input.txt")
  muls <- sapply(regmatches(x, gregexec("mul\\([0-9]{1,3},[0-9]{1,3}\\)", x)), \(z) paste(z, collapse = "+"))
  sum(sapply(muls, \(z) eval(parse(text = z))))
}

day03b <- function(x) {
  x <- readLines("day3_input.txt")
  dodont <- regmatches(x, gregexec("mul\\([0-9]{1,3},[0-9]{1,3}\\)|don't\\(\\)|do\\(\\)", x))
  solver(unlist(ops))
}

solver <- function(z) {
  total <- 0
  dodonts <- 1
  for (op in z) {
    if (op == "do()") {
      dodonts <- 1
    } else if (op == "don't()") {
      dodonts <- 0
    } else {
      total <- total + dodonts*eval(parse(text = op))
    }
  }
  total
}