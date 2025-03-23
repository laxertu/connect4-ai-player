import json
import logging
from json import JSONDecodeError

from cleo.commands.command import Command
from cleo.application import Application
from cleo.helpers import argument, option

from scoring_function import scoring_function
from facade import GameWrapper

def main(api_host: str, player_name: str):
    game_wrapper = GameWrapper(api_host, player_name)
    game_wrapper.game.custom_scoring_function = scoring_function
    my_game = game_wrapper.game

    print(f'Visit {api_host}/client/?sid={game_wrapper.session_id}')
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


class Main(Command):
    default_player_name = "Unnamed Player"
    name = "start"
    description = "Start a game"

    options = [
        option(
            "host",
            description="Host to connect to",
            default="https://connect4-api.onrender.com",
            flag=False,
        )
    ]

    def handle(self):
        #host = self.ask(f'Connect to [Default: {Main.default_host}]', default=self.default_host)
        host = self.option("host")
        player_name = self.ask(f'Player name [Default: {Main.default_player_name}]', default=self.default_player_name)
        self.line(f'Connecting to {host}')
        main(host, player_name)




app = Application()
app.add(Main())

if __name__ == '__main__':
    app.run()