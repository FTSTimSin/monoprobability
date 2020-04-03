import random

Board = {
    0: "GO",
    1: "Mediterranean Avenue",
    2: "CC 1",
    3: "Baltic Avenue",
    4: "Arctic Avenue",
    5: "Income Tax",
    6: "Reading Railroad",
    7: "Massachusetts Avenue",
    8: "Oriental Avenue",
    9: "Chance 1",
    10: "Gas Company",
    11: "Vermont Avenue",
    12: "Connecticut Avenue",
    13: "Jail",
    14: "Auction/Highest Rent",
    15: "Maryland Avenue",
    16: "St. Charles Place",
    17: "Electric Company",
    18: "States Avenue",
    19: "Virginia Avenue",
    20: "Pennsylvania Railroad",
    21: "St. James Place",
    22: "CC 2",
    23: "Tennessee Avenue",
    24: "New York Avenue",
    25: "New Jersey Avenue",
    26: "Free Parking",
    27: "Kentucky Avenue",
    28: "Chance 2",
    29: "Indiana Avenue",
    30: "Illinois Avenue",
    31: "Michigan Avenue",
    32: "Bus Ticket",
    33: "B&O Railroad",
    34: "Atlantic Avenue",
    35: "Ventnor Avenue",
    36: "Water Works",
    37: "Marvin Gardens",
    38: "California Avenue",
    39: "Go To Jail",
    40: "Pacific Avenue",
    41: "South Carolina Avenue",
    42: "North Carolina Avenue",
    43: "CC 3",
    44: "Pennsylvania Avenue",
    45: "Short Line",
    46: "Chance 3",
    47: "Birthday Gift",
    48: "Florida Avenue",
    49: "Park Place",
    50: "Luxury Tax",
    51: "Boardwalk"
}


class Game:
    def __init__(self, game_limit: int):
        self._board = Board
        self._player_space = 0
        self._turn_count = 0
        self._double_count = 0
        self._total_double = 0
        self._game_count = 0
        self._game_limit = game_limit
        self._total_turn = 0
        self._double_jail = 0
        self._stats = []
        for value in self._board.values():
            self._stats.append([value, 0])

    def play(self) -> None:
        if self._turn_count == 40:
            self._player_space = 0
            self._game_count += 1
            self._turn_count = 0

        roll = dice_roll()

        if roll[2] == 4 or roll[2] == 5 or roll[2] == 6:
            self._player_space = (self._player_space + roll[0] + roll[1]) % 52
        else:
            self._player_space = (self._player_space +
                                  roll[0] + roll[1] + roll[2]) % 52
        if "Chance" in self._board[self._player_space]:
            self._chance()
        if "CC" in self._board[self._player_space]:
            self._cc()
        if self._player_space == 39:
            self._player_space = 13

        self._total_turn += 1

        # double
        if roll[0] == roll[1]:
            self._double_count += 1
            self._total_double += 1
            # triple double jail
            if self._double_count == 3:
                self._player_space = 13
                self._double_jail += 1
        else:
            self._double_count = 0
            self._turn_count += 1

        amount = self._stats[self._player_space][1] + 1
        self._stats[self._player_space][1] = amount

        print(f"Game {self._game_count}, Turn {self._turn_count} done.")

    def game_over(self) -> bool:
        if self._game_count >= self._game_limit:
            return True

    def print_results(self) -> None:
        for stats in self._stats:
            print(f"{stats[0]}\t"
                  f"{round(((stats[1] / self._total_turn) * 100), 4)}%\t"
                  f"{stats[1]}")
        print(f"Total Turns: {self._total_turn}")
        print(f"Amount of Doubles: {self._total_double}")
        print(f"Amount of Triple Doubles; {self._double_jail}")

    def _chance(self) -> None:
        chance = random.randint(1, 16)
        # Advance to Go
        if chance == 1:
            self._player_space = 0

        # Advance to Illinois
        elif chance == 2:
            self._player_space = 30

        # Advance to St. Charles
        elif chance == 3:
            self._player_space = 16

        # Advance to nearest utility
        elif chance == 4:
            while self._player_space not in (10, 17, 36):
                self._player_space = (self._player_space + 1) % 52

        # Advance to nearest railroad
        elif chance == 5 or chance == 6:
            while self._player_space not in (6, 20, 33, 45):
                self._player_space = (self._player_space + 1) % 52

        # Go back three spaces
        elif chance == 8:
            self._player_space -= 3

        # Go to Jail
        elif chance == 9:
            self._player_space = 13

        # Trip to Reading Railroad
        elif chance == 12:
            self._player_space = 6

        # Trip to Boardwalk
        elif chance == 13:
            self._player_space = 51

    def _cc(self) -> None:
        cc = random.randint(1, 16)
        # Advance to Go
        if cc == 1:
            self._player_space = 0

        # Go to Jail
        elif cc == 6:
            self._player_space = 13


def dice_roll() -> (int, int, int):
    first = random.randint(1, 6)
    second = random.randint(1, 6)
    third = random.randint(1, 6)
    numbers = (first, second, third)
    return numbers


def main():
    game = Game(1000000)
    while not game.game_over():
        game.play()
    game.print_results()


if __name__ == "__main__":
    main()
