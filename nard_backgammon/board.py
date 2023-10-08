"""
:authors: cmdtorch
:license: MIT, see LICENSE file

:copyright: (c) 2023 cmdtorch
"""

from dataclasses import dataclass
from typing import Tuple, Optional, List
from .player import Player
from .exceptions import NardError


@dataclass
class Move:
    """
    Move class for Nard game
    """
    source: int
    direction: Optional[int] = None

    def __repr__(self):
        return f'[from: {self.source}, to: {self.direction}'


class Board:
    """
    Board for Nard game
    """

    def __init__(self):
        self.slots: Tuple[int, ...] = self._generate_slots()
        self._white_off: int = 0
        self._black_off: int = 0

    @property
    def white_off(self) -> int:
        """
        Number of white checkers offed from the board
        :return: number of checkers
        """
        return self._white_off

    @property
    def black_off(self) -> int:
        """
        Number of black checkers offed from the board
        :return: number of checkers
        """
        return self._black_off

    def add_move(self, player: Player, move: Move) -> Tuple[int, ...]:
        """
        Apply move on the board
        :param player: the player who played
        :param move: move for apply
        :return: new state of slots
        """
        slots = list(self.player_pov_slots(player))
        slots[move.source] = slots[move.source] + (1 if player == Player.BLACK else -1)
        if move.direction:
            slots[move.direction] = slots[move.direction] + (-1 if player == Player.BLACK else 1)
        else:
            if player == Player.WHITE:
                self._white_off += 1
            else:
                self._black_off += 1

        self._set_new_slots(player, slots)
        return self.slots

    def off(self, player: Player, source: int) -> None:
        """
        Off checker from the board
        :param player: the player who played
        :param source: source of checker
        :return: None
        """
        if not self.is_off_possible(player):
            raise NardError('There are checkers that are not at home')

        slots = list(self.player_pov_slots(player))
        slots[source] = slots[source] + (1 if player == Player.BLACK else -1)
        if player == Player.WHITE:
            self._white_off += 1
        else:
            self._black_off += 1

        self._set_new_slots(player, slots)
        # distance = 24 - source

    def get_valid_moves(self, player: Player, dices: Tuple[int]) -> Optional[List[Move]]:
        """
        Get list of valid moves.
        :param player: the player who played
        :param dices: dice number for move
        :return: list of valid moves
        """

        def player_piece_value():
            return 1 if player == Player.BLACK else -1

        def is_unacceptable_mars(slots, source: int, direction: int) -> bool:
            slots_after_move = list(slots)
            slots_after_move[source] = slots_after_move[source] + player_piece_value()
            slots_after_move[direction] = slots_after_move[direction] + player_piece_value()
            slots_after_move_handler = [1 if s > 0 else -1 if s < 0 else 0
                                        for s in slots_after_move]
            opponent_value = -1 if Player.WHITE == player else 1

            checkers_in_row = 0
            for i, s in enumerate(slots_after_move_handler):
                if player.WHITE and s > 0 or player.BLACK and s < 0:
                    checkers_in_row += 1
                    if checkers_in_row < 6:
                        continue
                    if i <= 12 and opponent_value not in slots_after_move_handler[0:13] or \
                            i >= 13 and opponent_value not in slots_after_move_handler[14:24] and\
                            -1 not in slots_after_move_handler[0:13]:
                        return True
                else:
                    checkers_in_row = 0

            return False

        player_view_slots = self.player_pov_slots(player)
        # CHECK FOR MOVE CHECKERS
        moves = []
        for index, slot in enumerate(player_view_slots):
            if not self.is_player_cell(player, slot):
                continue
            for dice in dices:
                try:
                    direction = index + dice
                    moved_slot = player_view_slots[direction]
                    if moved_slot != 0 and not self.is_player_cell(player, moved_slot):
                        continue
                    if not is_unacceptable_mars(player_view_slots, index, direction):
                        moves.append(Move(index, direction))
                except IndexError:
                    pass

        # CHECK FOR OFF CHECKERS
        if not self.is_off_possible(player):
            return moves

        off_moves = []
        home = list(player_view_slots[18:24])
        for index, slot in enumerate(home):
            if not self.is_player_cell(player, slot):
                continue

            for dice in dices:
                if 6 - index == dice:
                    off_moves.append(Move(index + 18, None))
                elif not moves:
                    off_moves.append(Move(index + 18, None))

        if off_moves:
            return off_moves
        return moves

    def is_off_possible(self, player: Player) -> bool:
        """
        Checking whether a player can off his checkers
        :param player: the player for check
        :return: `True` or `False`
        """
        slots_exclude_home = list(self.player_pov_slots(player))[0:18]
        match player:
            case Player.WHITE:
                if [cell for cell in slots_exclude_home if cell > 0]:
                    return False
            case Player.BLACK:
                if [cell for cell in slots_exclude_home if cell < 0]:
                    return False
        return True

    def player_pov_slots(self, player: Player) -> Tuple[int, ...]:
        """
        Slots by the player point of view
        :param player: the player for pov
        :return: slots list
        """
        if player == Player.BLACK:
            slots = list(self.slots)
            first_half = slots[0:12]
            return tuple(slots[12:24] + first_half)
        return self.slots

    def _set_new_slots(self, player: Player, new_slots: List[int]) -> None:
        if player == Player.BLACK:
            first_half = new_slots[0:12]
            new_slots = tuple(new_slots[12:24] + first_half)
        self.slots = tuple(new_slots)

    @staticmethod
    def is_player_cell(player: Player, slot: int) -> bool:
        """
        Check is has player piece in slot
        :param player: player for piece
        :param slot: slot number
        :return: `True` or `False`
        """
        if slot == 0:
            return False

        if player == Player.BLACK and slot < 0 \
                or player == Player.WHITE and slot > 0:
            return True
        return False

    @staticmethod
    def _generate_slots():
        slots = tuple(15 if i == 0 else
                      -15 if i == 12 else 0 for i in range(24))
        return slots

    def __repr__(self):
        return f'Slots: {self.slots} |' \
               f' White checkers offed: {self.white_off} |' \
               f' Black checkers offed: {self.black_off}'


def get_distance(move: Move) -> int:
    """
    Delta of move
    :param move: move
    :return: delta
    """
    if move.direction > move.source:
        return move.direction - move.source
    return (24 - move.source) + move.direction
