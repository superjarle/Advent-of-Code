solve_day_17 <- function(input) {
  matrix <- input |>
    strsplit("") |>
    unlist() |>
    as.numeric() |>
    matrix(nrow = length(input)) |>
    t()
  
  
  # pos row, pos col, dir row, dir col, consecutive steps
  start_state <- c(1L, 1L, 0L, 0L, 0L)
  goal_state <- c(nrow(matrix), ncol(matrix), 0L, 0L, 0L)
  
  # Part One
  print(dijkstra(matrix, start_state, goal_state))
  # Part Two
  print(dijkstra(matrix, start_state, goal_state,
                 min_steps = 4L,
                 max_steps = 10L))
}

make_key <- function(state) {
  key <- state |>
    unlist() |>
    paste(collapse = ",")
}

# This is the slowest part, iterating over the queue with sapply -
insert_in_order <- function(queue, state) {
  index <- which(sapply(queue, function(x) x$cost) > state$cost)[1]
  if (is.na(index)) {
    queue <- c(queue, list(state))
  } else {
    queue <- append(queue, list(state), index - 1)
  }
  return(queue)
}

dijkstra <- function(matrix, start, goal, min_steps = 1L, max_steps = 3L) {
  dirs <- list(
    "U" = c(-1L,0L),
    "D" = c(1L, 0L),
    "L" = c(0L, -1L),
    "R" = c(0L, 1L)
  )
  
  # Heat loss/cost in env for hashed lookup
  costs <- new.env()
  start_key <- make_key(start)
  costs[[start_key]] <- 0L
  
  # List as first-in-first-out queue
  queue <- list(list(state = start, cost = 0L))
  
  
  while(length(queue) > 0L) {
    # Dequeue from the front of the queue
    curr_state <- queue[[1L]]$state
    queue <- queue[-1L]
    
    # Read the current cost
    curr_key <- make_key(curr_state)
    curr_cost <- costs[[curr_key]]
    
    curr_row  <- curr_state[[1L]]
    curr_col  <- curr_state[[2L]]
    curr_dir  <- c(curr_state[[3L]], curr_state[[4L]])
    curr_step <- curr_state[[5L]]
    
    # Return if reached the goal
    if (curr_row == goal[[1]] & curr_col == goal[[2]]) {
      return(curr_cost)
    }
    
    # Otherwise try each valid direction
    for (next_dir in dirs) {
      # Skip backwards direction
      if (identical(-next_dir, curr_dir)) next
      # Skip same direction at max steps
      if (identical(next_dir, curr_dir) & curr_step == max_steps) next
      # If going in a new direction, take the minimum steps
      if (!identical(next_dir, curr_dir)) {
        
        next_dist <- min_steps
        next_step <- next_dist
        
      } else {
        # otherwise take just 1
        next_dist <- 1L
        next_step <- curr_step + next_dist
      }
      
      next_row <- curr_row + next_dist * next_dir[[1]]
      next_col <- curr_col + next_dist * next_dir[[2]]
      
      # Skip if out of bounds
      if (min(next_row, next_col) < 1 |
          next_row > nrow(matrix) |
          next_col > ncol(matrix)) {
        next
      }
      
      next_state <- c(next_row, next_col,
                      next_dir[[1]], next_dir[[2]],
                      next_step)
      
      next_cost <- curr_cost
      for (dist in 1:next_dist) {
        next_row <- curr_row + dist * next_dir[[1]]
        next_col <- curr_col + dist * next_dir[[2]]
        next_cost <- next_cost + as.numeric(matrix[next_row, next_col])
      }
      
      next_key <- make_key(next_state)
      # next_cost <- curr_cost + as.numeric(matrix[next_row, next_col])
      
      if (is.null(costs[[next_key]]) || next_cost < costs[[next_key]]) {
        # Add new state to the queue and costs lookup
        costs[[next_key]] <- next_cost
        queue <- insert_in_order(queue, list(state = next_state, cost = next_cost))
      }
    }
  }
}