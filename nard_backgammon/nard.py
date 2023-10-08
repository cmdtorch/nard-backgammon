"""
:authors: cmdtorch
:license: MIT, see LICENSE file

:copyright: (c) 2023 cmdtorch
"""

import random
from typing import Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass

from .board import Board, Move, get_distance
from .player import Player
from .exceptions import NardError


@dataclass
class NardOutcome:
    """
    Nard Outcome data
    """
    winner: Player


class NardState(Enum):
    """
    Nard Game State
    """
    FIRST_ROLL = 'first roll'
    PLAYING = 'playing'
    ENDED = 'ended'


class Nard:
    """
    Nard Game main class
    """

    def __init__(self, board: Board, state: NardState, player_turn: Optional[Player] = None):
        self.board: Board = board
        self.state: NardState = state
        self.player_turn: Optional[Player] = player_turn
        self.dice_nums: Optional[Tuple[int, ...]] = None
        self.outcome: Optional[NardOutcome] = None

    @classmethod
    def new(cls, first_roll_player: Player = None):
        """
        Create new Nard game instance
        :param first_roll_player: Player for first roll
        (Must first_roll() if first_roll_player is None)
        """
        board = Board()

        if first_roll_player:
            state = NardState.PLAYING
        else:
            state = NardState.FIRST_ROLL

        game = cls(board, state, first_roll_player)
        game.dice_nums = random_nums()

        return game


    def get_valid_moves(self, player: Player = None) -> List[Move]:
        """
        Get list of valid moves for player (for turn player if player is None)
        :param player: a player from whom you need to find out possible moves
        :return: list of moves for the player
        """
        if player is None:
            player = self.player_turn
        if not self.dice_nums:
            raise NardError('Dices is not rolled')
        return self.board.get_valid_moves(player, self.dice_nums)

    def first_roll(self) -> Player:
        """
        First roll to find out which player starts first
        :return: The player who won the first roll
        """
        print(self.state != NardState.FIRST_ROLL)
        if self.state != NardState.FIRST_ROLL:
            raise NardError("The first roll has already been made")

        while True:
            dices = random_nums()
            if dices[0] != dices[1]:
                break

        self.dice_nums = dices
        self.player_turn = Player.WHITE if dices[0] > dices[1] else Player.BLACK
        self.state = NardState.PLAYING
        return self.player_turn

    def play_move(self, move: Move) -> None:
        """
        Make the move
        :param move: move for turn player
        :return: None
        """
        # VALIDATION
        if not self.dice_nums:
            raise NardError('All moves is played')

        if move not in self.get_valid_moves(self.player_turn):
            raise NardError(f'Move is not valid: {move}')

        # PLAYING
        if move.direction:
            self.board.add_move(self.player_turn, move)
            self._pop_played_dice_num(get_distance(move))
        else:
            self.board.off(self.player_turn, move.source)
            for num in range(24-move.source, 7):
                if num in self.dice_nums:
                    self._pop_played_dice_num(num)
                    break

        # FINISH TURN
        if not self.dice_nums:
            self._set_next_player_turn(self.player_turn)
            self._roll_dice()

        # OUTCOME
        if self.board.white_off == 15:
            self.outcome = NardOutcome(winner=Player.WHITE)
        elif self.board.black_off == 15:
            self.outcome = NardOutcome(winner=Player.BLACK)

        if self.outcome:
            self.state = NardState.ENDED

    def skip(self) -> None:
        """
        Skip turn (only if the player has no possible moves)
        :return: None
        """
        if self.board.get_valid_moves(self.player_turn, self.dice_nums):
            raise NardError('Skip is not available')
        self._set_next_player_turn(self.player_turn)
        self._roll_dice()


    def _set_next_player_turn(self, player: Player):
        self.player_turn = Player.BLACK if player == Player.WHITE else Player.WHITE

    def _pop_played_dice_num(self, num):
        nums = list(self.dice_nums)
        nums.remove(num)
        self.dice_nums = tuple(nums)

    def _roll_dice(self):
        dices = random_nums()
        if dices[0] == dices[1]:
            self.dice_nums = dices * 2
            return self.dice_nums

        self.dice_nums = dices
        return self.dice_nums


def random_nums():
    return (
        random.SystemRandom().randrange(1, 6),
        random.SystemRandom().randrange(1, 6),
    )


def get_random_move(moves: List[Move]) -> Move:
    """
    Get random move from move list
    :param moves: valid move list
    :return: randomly selected move
    """
    if len(moves) > 1:
        return moves[random.SystemRandom().randrange(0, len(moves)-1)]
    return moves[0]


def board_to_str(nard: Nard) -> str:
    """
    Visual display of the board as a line
    :param nard: Nard
    :return: board pic
    """
    def cell_to_str(value: int):
        if value == 0:
            return '  '
        return 'o ' if value > 0 else 'x '

    def count_to_str(value: int):
        value = abs(value)
        if value > 1:
            return f'{value} ' if value < 10 else str(value)
        return '  '

    sections = []
    sections_nums = []
    for i in range(0, 4):
        section = []
        section_nums = []
        for cell in nard.board.slots[6 * i:6 * i + 6]:
            section.append(f'{cell_to_str(cell)}')
            section_nums.append(f'{count_to_str(cell)}')
        if i in [0, 1]:
            section.reverse()
            section_nums.reverse()
        sections.append(section)
        sections_nums.append(section_nums)

    return f'''
            ||12-11-10-9--8--7-||6--5--4--3--2--1-||
            ||{' '.join(sections[1])}||{' '.join(sections[0])}||
            ||{' '.join(sections_nums[1])}||{' '.join(sections_nums[0])}||
            ||                 ||                 || White off: {nard.board.white_off}
            ||                 ||                 || Black off: {nard.board.black_off}
            ||                 ||                 || Dices: {nard.dice_nums}
            ||{' '.join(sections_nums[2])}||{' '.join(sections_nums[3])}||
            ||{' '.join(sections[2])}||{' '.join(sections[3])}||
            ||13-14-15-16-17-18||19-20-21-22-23-24||
    '''
