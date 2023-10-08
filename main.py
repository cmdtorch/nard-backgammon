from nard_backgammon import (
    Nard,
    NardState,
    Player,
    get_random_move,
    board_to_str)


# If the first_player is None, then the starting
# player is found on the first roll `first_roll()`
game = Nard.new(first_roll_player=Player.WHITE)

while True:

    match game.state:
        # If first_roll_player is None then
        # NardState is will be FIRST_ROLL at the init
        case NardState.FIRST_ROLL:
            game.first_roll()

        case NardState.PLAYING:
            # get valid moves for active player
            moves = game.get_valid_moves()
            if not moves:
                game.skip()
                continue
            move = get_random_move(moves)
            game.play_move(move)
            print(board_to_str(game))

        case NardState.ENDED:
            print(f'Winner: {game.outcome.winner}')
            break
