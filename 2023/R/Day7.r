library(dplyr)
library(tidyr)
library(stringr)

cards <- read.csv2("day7.txt", header = FALSE, sep = " ")

# Separate the first column into individual card columns
cards <- cards %>%
  separate(V1, into = c("c1", "c2", "c3", "c4", "c5"), sep = 1:4)

# Define a function for dec hands. 
dec_hand <- function(hand) {
  compo <- str_split(hand, "") %>% 
    unlist() %>% 
    tibble(card = .) %>% 
    group_by(card) %>% 
    count() %>% 
    arrange(-n) %>% 
    pull(n)
  if(compo[1] == 5) return("1:5k")
  if(compo[1] == 4) return("2:4k")
  if(compo[1] == 3 && compo[2] == 2) return("3:full")
  if(compo[1] == 3) return("4:3k")
  if(compo[1] == 2 && compo[2] == 2) return("5:2p")
  if(compo[1] == 2) return("6:2k")
  return("7:1k")
}

# Apply the function and other transformations
cards <- cards %>%
  rowwise() %>%
  mutate(hand = paste(c1, c2, c3, c4, c5, sep = ""),
         type = dec_hand(hand)) %>%
  ungroup() %>%
  mutate(across(starts_with("c"), ~ ordered(., levels = c("A", "K", "Q", "J", "T", as.character(9:2)))))

# Arrange and calculate the rank
cards <- cards %>%
  arrange(type, c1, c2, c3, c4, c5) %>%
  mutate(rank = (n() - row_number() + 1))

# Calculate the final sum
part1 <- cards %>%
  summarise(total = sum(rank * V2))

# View the result
print(part1)



## Part 2 with the jokers.. 
cards <- cards %>%
  mutate(across(starts_with("c"), ~ ordered(., levels = c("A", "K", "Q", "T", as.character(9:2), "J"))))

# Another dec_hand.. 
dec_hand2 <- function(hand) {
  compo <- str_split(hand, "") %>%
    unlist() %>%
    tibble(card = .) %>%
    group_by(card) %>%
    count() %>%
    arrange(-n)
  
  if (all(compo$card == "J")) {
    return("1:5k")
  }
  
  if (any(compo$card == "J")) {
    new_card <- compo %>%
      filter(card != "J") %>%
      pull(card) %>%
      first()
    compo <- compo %>%
      mutate(card = if_else(card == "J", new_card, card)) %>%
      group_by(card) %>%
      summarise(n = sum(n)) %>%
      arrange(-n)
  }
  
  compo <- compo %>%
    pull(n)
  
  if (compo[1] == 5) return("1:5k")
  if (compo[1] == 4) return("2:4k")
  if (compo[1] == 3 && compo[2] == 2) return("3:full")
  if (compo[1] == 3) return("4:3k")
  if (compo[1] == 2 && compo[2] == 2) return("5:2p")
  if (compo[1] == 2) return("6:2k")
  return("7:1k")
}

# Apply the new function
cards <- cards %>%
  rowwise() %>%
  mutate(hand = paste(c1, c2, c3, c4, c5, sep = ""),
         type = dec_hand2(hand)) %>%
  ungroup()

# Arrange and calculate the rank
cards <- cards %>%
  arrange(type, c1, c2, c3, c4, c5) %>%
  mutate(rank = (n() - row_number() + 1))

# Calculate the final sum
part2 <- cards %>%
  summarise(total = sum(rank * V2))

# View the result
print(part2)
