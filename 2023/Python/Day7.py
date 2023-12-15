## imnport the file
with open(file_path, 'r') as file:
    file_content = file.readlines()
    

## Play the game


class PokerGame:
    def __init__(self, file_content):
        self.hands = self.parse_input(file_content)

    @staticmethod
    def parse_input(file_content):
        lines = [line.strip('\r\n') for line in file_content]
        lines = [line.split() for line in lines]
        return [(hand, int(bid)) for hand, bid in lines]

    @staticmethod
    def hand_type(hand):
        groups = defaultdict(int)
        for c in hand:
            groups[c] += 1

        L = [(v, k) for k, v in groups.items()]
        L.sort(reverse=True)

        if L[0][0] == 5:
            base = 7
        elif L[0][0] == 4:
            base = 6
        elif L[0][0] == 3 and L[1][0] == 2:
            base = 5
        elif L[0][0] == 3:
            base = 4
        elif L[0][0] == 2 and L[1][0] == 2:
            base = 3
        elif L[0][0] == 2:
            base = 2
        elif L[0][0] == 1:
            base = 1
        else:
            assert 0

        return 10**base

    @staticmethod
    def score_hand1(hand):
        base = PokerGame.hand_type(hand)
        cards = '23456789TJQKA'
        s = ''.join(f'{cards.index(c):02d}' for c in hand)
        return int(str(base) + s)

    @staticmethod
    def hand_cmp(a, b, score_function):
        a_score = score_function(a[0])
        b_score = score_function(b[0])
        if a_score < b_score:
            return -1
        if a_score == b_score:
            return 0
        return 1

    def part1(self):
        hands = copy.deepcopy(self.hands)
        hands.sort(key=cmp_to_key(lambda a, b: PokerGame.hand_cmp(a, b, PokerGame.score_hand1)))
        total = 0
        for i, (hand, bid) in enumerate(hands):
            total += (i + 1) * bid
        return total

    @staticmethod
    def score_hand2(hand):
        cards = 'J23456789TQKA'
        base = max(PokerGame.hand_type(hand.replace('J', c)) for c in cards[1:])
        s = ''.join(f'{cards.index(c):02d}' for c in hand)
        return int(str(base) + s)

    def part2(self):
        hands = copy.deepcopy(self.hands)
        hands.sort(key=cmp_to_key(lambda a, b: PokerGame.hand_cmp(a, b, PokerGame.score_hand2)))
        total = 0
        for i, (hand, bid) in enumerate(hands):
            total += (i + 1) * bid
        return total

# Create an instance of the PokerGame class with the file content
poker_game = PokerGame(file_content)

# Run both parts of the program
part1 = poker_game.part1()
part2 = poker_game.part2()

part1, part2

