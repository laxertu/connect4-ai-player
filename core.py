from collections.abc import Callable
from dataclasses import dataclass
import random
from easyAI import AI_Player, Negamax, Human_Player
from easyAI.TwoPlayerGame import TwoPlayerGame

class FullColumnException(Exception):
    ...


class Board:

    def __init__(self, width: int = 8, height: int = 8, filler: str = '-'):
        self.w = width
        self.h = height
        self.emptyFiller = filler
        self.data: list = []
        self.fillers_used = set()
        self.data = [self.emptyFiller] * height
        for x in range(height):
            self.data[x] = [self.emptyFiller] * width

    @property
    def width(self):
        return self.w

    @property
    def height(self):
        return self.h

    def make_turn(self, col, filler):
        self.update(col, filler)

    def update(self, col, filler):
        cell = self.get_first_free_cell(col)
        self.fillers_used.add(filler)
        self.data[cell][col] = filler

    def is_there_a_winner(self):
        for filler in [x for x in self.fillers_used if x != self.emptyFiller]:
            if self.find_filler_occurrencies(filler, 4) > 0:
                return True
        return False

    def is_over(self):
        return self.is_there_a_winner()

    def find_filler_occurrencies(self, filler, num):
        return self.substring_count(filler * num)

    def substring_count(self, string_to_find):
        result = 0
        for line in self.data:
            result += ''.join(line).count(string_to_find)

        for col in [[row[i] for row in self.data] for i in range(len(self.data[0]))]:
            result += ''.join(col).count(string_to_find)

        for diagonal in self.diagonals():
            result += ''.join(diagonal).count(string_to_find)

        return result

    def diagonals(self):
        '''
        credits: https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
        :return:
        '''
        result = []

        cols = len(self.data)
        rows = len(self.data[0])

        fdiag = [[] for i in range(cols + rows - 1)]
        bdiag = [[] for i in range(len(fdiag))]
        min_bdiag = -cols + 1

        for y in range(0, cols):
            for x in range(rows):
                fdiag[x + y].append(self.data[y][x])
                bdiag[-min_bdiag + x - y].append(self.data[y][x])

        for line in bdiag + fdiag:
            result.append(''.join(line))

        random.shuffle(result)
        return result

    def get_first_free_cell(self, col: int) -> int:

        result = self.h - 1
        done = False

        col = int(col)
        if (col < 0) or (col > self.w):
            raise Exception('invalid col')

        while not done:
            try:
                if self.data[result][col] == self.emptyFiller:
                    done = True
                else:
                    result = result - 1
            except IndexError:
                raise FullColumnException('No free cells in col ' + str(col))

        return result


def default_scoring_function(board: Board, filler_player: str, filler_opponent: str) -> int:
    if board.find_filler_occurrencies(filler_player, 4) > 0:
        return 50000

    if board.find_filler_occurrencies(filler_opponent, 4) > 0:
        return -50000

    return 0

@dataclass
class Player(AI_Player):
    name: str
    filler: str
    #fillers: list[str]
    #uuid https://docs.python.org/3/library/uuid.html

    @property
    def id(self) -> str:
        return str(id(self))


    def __init__(self, name: str, filler: str):
        super().__init__(Negamax(4), name)
        self.name = name
        self.filler = filler


class EasyAIGame(TwoPlayerGame):

    def __init__(self, board: Board, players: list[Player]):
        self.board: Board = board
        self.players: list[Player] = players
        self.current_player = 1
        self.num_rounds: int = 0
        self.activated_mods = set()
        self.custom_scoring_function: Callable[[Board, str, str], int] = default_scoring_function



    def possible_moves(self):
        result = []
        for x in range(0, self.board.w):
            try:
                self.board.get_first_free_cell(x)
                result.append(x)
            except FullColumnException:
                pass

        return result

    def make_move(self, move: str):
        self.board.make_turn(int(move), self.player.filler)

    def is_over(self):
        return self.board.is_there_a_winner()

    #----

    def fillers(self) -> dict[int: list[str]]:
        return {
            1: [self.players[0].filler],
            2: [self.players[1].filler]
        }


    def scoring(self) -> int:
        return self.custom_scoring_function(self.board, self.player.filler, self.opponent.filler)



def create_game(game_data: dict):
    # board_data = game_data['board']
    my_filler = game_data['game']['players'][0]['filler']
    adv_filler = game_data['game']['players'][1]['filler']

    player1 = Player(name='player 1', filler=my_filler)
    player2 = Player(name='player 2', filler=adv_filler)

    board = Board()

    game = EasyAIGame(board = board, players = [player1, player2])
    return game

