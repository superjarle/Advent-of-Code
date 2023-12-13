# Read input data from file
puzzleinput <- readLines("input.txt")

# Split input into separate patterns
patterns <- list()
patternIndex <- 1
currentPattern <- c()

for (i in seq_along(puzzleinput)) {
  if (nchar(puzzleinput[i]) == 0) {
    patterns[[patternIndex]] <- currentPattern
    patternIndex <- patternIndex + 1
    currentPattern <- c()
  } else if (i == length(puzzleinput)) {
    currentPattern <- append(currentPattern, puzzleinput[i])
    patterns[[patternIndex]] <- currentPattern
    patternIndex <- patternIndex + 1
    currentPattern <- c()
  } else {
    currentPattern <- append(currentPattern, puzzleinput[i])
  }
}

# Function to transform rows to columns
transformToColumns <- function(x) {
  splitStr <- strsplit(x, "") |> as.data.frame() |> unname()
  transposed <- t(splitStr)
  apply(transposed, MARGIN = 2, FUN = function(y) { Reduce(paste0, y) })
}

# Function to check symmetry
checkSymmetry <- function(x, lineID) {
  upperPart <- x[1:lineID]
  lowerPart <- rev(x[(lineID + 1):(lineID + length(upperPart))])
  all(upperPart == lowerPart, na.rm = TRUE)
}

# Function to check for partial symmetry in a pattern
checkPartialSymmetry <- function(pattern, lineIndex) {
  upperPart <- pattern[1:lineIndex]
  lowerPart <- pattern[(lineIndex + 1):(lineIndex + length(upperPart))]

  # Ensure upper and lower parts are of equal length
  upperPart <- upperPart[!is.na(rev(lowerPart))]
  lowerPart <- rev(lowerPart[!is.na(lowerPart)])

  # Check if there is exactly one mismatch
  if (length(unlist(strsplit(upperPart, ""))) == 
      sum(unlist(strsplit(upperPart, "")) == unlist(strsplit(lowerPart, ""))) + 1) {
    return(TRUE)
  } else {
    return(FALSE)
  }
}

# Calculate the solution
calculateSolution <- function(patterns, symmetryCheckFunction) {
  idLines <- c()
  idColumns <- c()
  
  for (pattern in patterns) {
    lines <- unlist(sapply(1:(length(pattern) - 1), function(i) symmetryCheckFunction(pattern, i)))
    columns <- unlist(sapply(1:(length(transformToColumns(pattern)) - 1), function(i) symmetryCheckFunction(transformToColumns(pattern), i)))
    
    if (any(!is.na(lines)) && any(lines)) {
      idLines <- c(idLines, which(lines))
    }
    
    if (any(!is.na(columns)) && any(columns)) {
      idColumns <- c(idColumns, which(columns))
    }
  }
  
  sum(idColumns) + sum(100 * idLines)
}
                             

# Solutions for Part 1 and Part 2
part1 <- calculateSolution(patterns, checkSymmetry)
part2 <- calculateSolution(patterns, checkPartialSymmetry)

# Print solutions
cat("Solution for part 1 is:", part1, "\n")
cat("Solution for part 2 is:", part2, "\n")
