import random

Board = {
    0: "GO",
    1: "Mediterranean Avenue",
    2: "CC 1",
    3: "Baltic Avenue",
    4: "Income Tax",
    5: "Reading Railroad",
    6: "Oriental Avenue",
    7: "Chance 1",
    8: "Vermont Avenue",
    9: "Connecticut Avenue",
    10: "Jail",
    11: "St. Charles Place",
    12: "Electric Company",
    13: "States Avenue",
    14: "Virginia Avenue",
    15: "Pennsylvania Railroad",
    16: "St. James Place",
    17: "CC 2",
    18: "Tennessee Avenue",
    19: "New York Avenue",
    20: "Free Parking",
    21: "Kentucky Avenue",
    22: "Chance 2",
    23: "Indiana Avenue",
    24: "Illinois Avenue",
    25: "B&O Railroad",
    26: "Atlantic Avenue",
    27: "Ventnor Avenue",
    28: "Water Works",
    29: "Marvin Gardens",
    30: "Go To Jail",
    31: "Pacific Avenue",
    32: "North Carolina Avenue",
    33: "CC 3",
    34: "Pennsylvania Avenue",
    35: "Short Line",
    36: "Chance 3",
    37: "Park Place",
    38: "Luxury Tax",
    39: "Boardwalk"
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

        self._player_space = (self._player_space + roll[0] + roll[1]) % 40
        if "Chance" in self._board[self._player_space]:
            self._chance()
        if "CC" in self._board[self._player_space]:
            self._cc()
        if self._player_space == 30:
            self._player_space = 10

        self._total_turn += 1

        # double
        if roll[0] == roll[1]:
            self._double_count += 1
            self._total_double += 1
            # triple double jail
            if self._double_count == 3:
                self._player_space = 10
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
            self._player_space = 24

        # Advance to St. Charles
        elif chance == 3:
            self._player_space = 11

        # Advance to nearest utility
        elif chance == 4:
            while self._player_space not in (12, 28):
                self._player_space = (self._player_space + 1) % 40

        # Advance to nearest railroad
        elif chance == 5:
            while self._player_space not in (5, 15, 25, 35):
                self._player_space = (self._player_space + 1) % 40

        # Go back three spaces
        elif chance == 8:
            self._player_space -= 3

        # Go to Jail
        elif chance == 9:
            self._player_space = 10

        # Trip to Reading Railroad
        elif chance == 12:
            self._player_space = 5

        # Trip to Boardwalk
        elif chance == 13:
            self._player_space = 39

    def _cc(self) -> None:
        cc = random.randint(1, 16)
        # Advance to Go
        if cc == 1:
            self._player_space = 0

        # Go to Jail
        elif cc == 6:
            self._player_space = 10


def dice_roll() -> (int, int):
    first = random.randint(1, 6)
    second = random.randint(1, 6)
    numbers = (first, second)
    return numbers


def main():
    game = Game(1000000)
    while not game.game_over():
        game.play()
    game.print_results()


if __name__ == "__main__":
    main()
