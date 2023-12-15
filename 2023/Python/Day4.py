## AOC 4

# Loading data

## Part 1


def calculate_points(scratchcard_lines):
    total_points = 0

    for line in scratchcard_lines:
        # Splitting the line to separate winning numbers from player's numbers
        parts = line.strip().split(' | ')
        winning_numbers = set(map(int, parts[0].split(':')[1].strip().split()))
        player_numbers = set(map(int, parts[1].strip().split()))

        # Finding the matching numbers
        matches = winning_numbers.intersection(player_numbers)

        # Calculating points for this card
        if matches:
            card_points = 1
            for _ in range(1, len(matches)):
                card_points *= 2
            total_points += card_points

    return total_points


sol1 = calculate_points(scratchcard_data)
sol1
# Part 2

def count_total_p2(scratchcard_lines):
    cards = []
    for line in scratchcard_lines:
        # Splitting the line to separate winning numbers from player's numbers
        parts = line.strip().split(' | ')
        winning_numbers = set(map(int, parts[0].split(':')[1].strip().split()))
        player_numbers = set(map(int, parts[1].strip().split()))
        cards.append((winning_numbers, player_numbers))

    # Dictionary to keep track of the number of copies for each card
    card_copies = {i: 1 for i in range(len(cards))}  # Initially, each card has one copy

    # Processing each card to determine additional copies won
    for i in range(len(cards)):
        winning_numbers, player_numbers = cards[i]
        matches = winning_numbers.intersection(player_numbers)
        num_matches = len(matches)

        # Incrementing the count of copies for subsequent cards
        for j in range(i + 1, min(i + num_matches + 1, len(cards))):
            card_copies[j] += card_copies[i]

    return sum(card_copies.values())

# Solution P2
sol2 = count_total_p2(scratchcard_data)
sol2
