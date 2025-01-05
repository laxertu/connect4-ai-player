from core import Board

def scoring_function(board: Board, filler_player: str, filler_opponent: str):

    mask = f'{board.emptyFiller}{filler_player * 3}{board.emptyFiller}'
    if board.substring_count(mask) > 1:
        return 50000

    mask = f'{board.emptyFiller}{filler_opponent * 3}{board.emptyFiller}'
    if board.substring_count(mask) > 1:
        return -50000

    if board.find_filler_lines_of_num(filler_player, 4) > 0:
        return 50000

    if board.find_filler_lines_of_num(filler_opponent, 4) > 0:
        return -50000

    result = 0

    result += 5 * board.find_filler_lines_of_num(filler_player, 3)
    result += 3 * board.find_filler_lines_of_num(filler_player, 2)

    result -= 5 * board.find_filler_lines_of_num(filler_opponent, 3)
    result -= 3 * board.find_filler_lines_of_num(filler_opponent, 2)

    mask = f'{board.emptyFiller}{filler_player * 3}'
    result += board.substring_count(mask) * 2

    mask = f'{board.emptyFiller}{filler_opponent * 3}'
    result -= board.substring_count(mask) * 2

    return result
