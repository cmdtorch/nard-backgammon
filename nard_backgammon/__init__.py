"""
:authors: cmdtorch
:license: MIT, see LICENSE file

:copyright: (c) 2023 cmdtorch
"""

version = '0.1.0'

from .nard import (Nard, NardState, NardOutcome, get_random_move, board_to_str)
from .board import Board
from .player import Player
from .exceptions import NardError

__authors__ = 'cmdtorch'
__version__ = version
__email__ = 'emil4154515@gmail.com'
