from core import Board

def scoring_function(board: Board, filler_player: str, filler_opponent: str):
    if board.find_filler_occurrencies(filler_player, 4) > 0:
        return 50000

    if board.find_filler_occurrencies(filler_opponent, 4) > 0:
        return -50000

    return 0