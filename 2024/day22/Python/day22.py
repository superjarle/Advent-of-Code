from time import time

# Start the timer
time_start = time()

# Constants
INPUT_FILE = "day22_input.txt"
MONKEY_MOD = 16777216  # Maximum monkey secret range
MONKEY_DAYS = 2000  # Number of secrets to generate per buyer

# Read buyer data from file
buyer_secrets = [int(line.strip()) for line in open(INPUT_FILE, "r")]

# Helper function to calculate the next monkey secret
def evolve_secret(secret):
    secret = (secret ^ (secret << 6)) % MONKEY_MOD
    secret = (secret ^ (secret >> 5)) % MONKEY_MOD
    secret = (secret ^ (secret << 11)) % MONKEY_MOD
    return secret

# Arrays for calculations
banana_secrets = [0] * (MONKEY_DAYS + 1)
banana_prices = [0] * (MONKEY_DAYS + 1)
price_changes = [0] * (MONKEY_DAYS + 1)
seen_patterns = [0] * (1 << 20)
banana_sales = [0] * (1 << 20)

# Calculate Part 1
monkey_total = 0
for buyer_id, initial_secret in enumerate(buyer_secrets, start=1):
    banana_secrets[0] = initial_secret
    banana_prices[0] = banana_secrets[0] % 10

    # Generate secrets and prices
    for day in range(1, MONKEY_DAYS + 1):
        banana_secrets[day] = evolve_secret(banana_secrets[day - 1])
        banana_prices[day] = banana_secrets[day] % 10
        price_changes[day] = banana_prices[day] - banana_prices[day - 1]

    # Sum the 2000th secret for Part 1
    monkey_total += banana_secrets[MONKEY_DAYS]

    # Map price change patterns to indices for optimization
    for day in range(4, MONKEY_DAYS + 1):
        # Explanation:
        # Each price change ranges from -9 to +9. By adding 9, the range shifts to 0 to 18.
        # This allows us to represent each change in 5 bits (since 2^5 = 32 covers the range).
        # We combine 4 consecutive changes into a single integer by left-shifting each change by
        # 15, 10, 5, and 0 bits respectively. This creates a unique 20-bit index for each pattern,
        # which is efficient for hashing and avoids tuple-based operations.
        pattern_hash = (((price_changes[day - 3] + 9) << 15) |
                        ((price_changes[day - 2] + 9) << 10) |
                        ((price_changes[day - 1] + 9) << 5) |
                        (price_changes[day] + 9))

        if seen_patterns[pattern_hash] != buyer_id:
            seen_patterns[pattern_hash] = buyer_id
            banana_sales[pattern_hash] += banana_prices[day]

# Output Part 1
print(f"Part 1: {monkey_total}  ({time() - time_start:.3f}s)")

# Calculate Part 2
max_bananas = max(banana_sales)

# Output Part 2
print(f"Part 2: {max_bananas}  ({time() - time_start:.3f}s)")
