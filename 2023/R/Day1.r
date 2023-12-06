# In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
getwd()
part1 = function(str) {
  ## This works but is clunky
  digit_locs = stringr::str_locate_all(str, "[:digit:]")
  min_digit = min(unlist(digit_locs))
  max_digit = max(unlist(digit_locs))
  first_digit = stringr::str_sub(str, start = min(unlist(digit_locs)), end =
                                   min_digit)
  last_digit = stringr::str_sub(str, start = max_digit, end = max_digit)
  return(as.numeric(paste0(first_digit, last_digit)))
}

day1 = readLines("day1.txt")
## Sum a list of elements with Reduce(), use lapply to vectorize get_digit
Reduce("+", lapply(day1, part1))



## Part 2
# Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
#
# Equipped with this new information, you now need to find the real first and last digit on each line. For example:

# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
#
# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.


part2 = function(str) {
  ## Helper named vector
  named_digits = c(
    "zero" = 0,
    "one" = 1,
    "two" = 2,
    "three" = 3,
    "four" = 4,
    "five" = 5,
    "six" = 6,
    "seven" = 7,
    "eight" = 8,
    "nine" = 9
  )
  
  ## For some reason you need this substitution
  ## If it's not there the code for my input is off by 2
  str = str |>
    stringr::str_replace_all(string = _, "one", "one1one") |>
    stringr::str_replace_all(string = _, "two", "two2two") |>
    stringr::str_replace_all(string = _, "three", "three3three") |>
    stringr::str_replace_all(string = _, "four", "four4four") |>
    stringr::str_replace_all(string = _, "five", "five5five") |>
    stringr::str_replace_all(string = _, "six", "six6six") |>
    stringr::str_replace_all(string = _, "seven", "seven7seven") |>
    stringr::str_replace_all(string = _, "eight", "eight8eight") |>
    stringr::str_replace_all(string = _, "nine", "nine9nine")
  
  ## Find all the digits in the word
  digit_locs = stringr::str_locate_all(str, "[:digit:]")
  min_digit_idx = min(unlist(digit_locs))
  max_digit_idx = max(unlist(digit_locs))
  
  ## Find all the word digits
  word_pattern = "one|two|three|four|five|six|seven|eight|nine"
  word_digit_locs = unlist(stringr::str_locate_all(str, word_pattern))
  word_digits = unlist(stringr::str_extract_all(str, word_pattern))
  min_word_idx = min(unlist(word_digit_locs))
  max_word_idx = max(unlist(word_digit_locs))
  
  ## test for lowest and highest positions
  if (min_digit_idx < min_word_idx) {
    first_digit = stringr::str_sub(str,
                                   start = min_digit_idx,
                                   end = min_digit_idx)
  }
  else{
    first_digit = unname(named_digits[word_digits[1]])
    
  }
  if (max_digit_idx > max_word_idx) {
    last_digit = stringr::str_sub(str, 
                                  start = max_digit_idx, 
                                  end = max_digit_idx)
  }
  else{
    last_digit = unname(named_digits[tail(word_digits, 1)])
  }
  return(as.numeric(paste0(first_digit, last_digit)))
}

Reduce("+", lapply(day1, part2))