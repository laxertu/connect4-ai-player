import sys
import json
import logging
from json import JSONDecodeError
from scoring_function import scoring_function

try:
    API_HOST = sys.argv[1]
except IndexError:
    API_HOST = 'http://127.0.0.1:8000'


from facade import GameWrapper

game_wrapper = GameWrapper(API_HOST)
game_wrapper.game.custom_scoring_function = scoring_function
my_game = game_wrapper.game


print(f'Visit {API_HOST}/client/?sid={game_wrapper.session_id}')
input('Press [ENTER] when ready')

# Rock and roll!
c = game_wrapper.start()
my_game.custom_scoring_function = scoring_function

try:

    for m in c:
        if m.event == 'ask_move':
            print()
            print("Move requested")
            try:
                my_game.current_player = 1
                my_game.board.data = json.loads(m.data)['payload']['board']
                game_wrapper.display_board()
                game_wrapper.send_move_response(my_game.player.ask_move(my_game))

            except JSONDecodeError as e:
                logging.warning(f'wrong json: {m.data}')
                input('We have to restart. Press [ENTER] to close the game')
                game_wrapper.end()
                exit(0)



        elif m.event == 'game_over':
            print()
            print('*** AND THE WINNER IS ***')
            print(json.loads(m.data)["payload"]["winner"])
            print()
            input('Press [ENTER] to close the game')
            game_wrapper.end()
            exit(0)

except KeyboardInterrupt:
    print('Closing...')
    game_wrapper.end()
    print('Done')
