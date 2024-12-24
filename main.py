import sys
import json
import logging
import traceback
from json import JSONDecodeError

import requests
from sseclient import SSEClient
from core import create_game
from scoring_function import scoring_function

try:
    API_HOST = sys.argv[1]
except IndexError:
    API_HOST = 'http://127.0.0.1:8000'


def send_move_response(response: int):

    print("Selected move", response)

    move_payload = {
        "type": "ask_move_rs",
        "payload": {'pos': response, 'sender_id': watch_id}
    }


    url = f'{API_HOST}/game/dispatch/{session_id}/{listener_id}'
    # print('ask move response', url, move_payload)
    requests.post(url, json=move_payload)
    my_game.make_move(response)
    my_game.switch_player()

def start_game():

    move_payload = {
        "type": "ask_move",
        "payload": {'sender_id': watch_id, 'payload': {'board': my_game.board.data}}
    }

    url = f'{API_HOST}/game/dispatch/{session_id}/{watch_id}'
    requests.post(url, json=move_payload)

try:
    payload = {
        "creator_name": input('Your name. Be original, you\'ll need to find yourself: '),
        "session_name": input('Session name. Same applies: '),
        "board_w": 8,
        "board_h": 8
    }
    input('I was kidding, named session are not currently supported. Press enter to continue.')
    print("creating game. This may take a while...")

    #print("creating match...", f'{API_HOST}/game/d_ai_battle')
    #print()
    raw = requests.put(f'{API_HOST}/game/d_ai_battle', json=payload)
    rsp = raw.json()
    #print(rsp)

    my_game = create_game(rsp)
    my_game.custom_scoring_function = scoring_function

    session_id, watch_id, listener_id = rsp['session_id'], rsp['stream'], rsp['notifications']

except Exception as e:
    print(traceback.format_exc())
    exit(0)


c = SSEClient(f'{API_HOST}/game/stream/{session_id}/{watch_id}')

print('Done')
print(f'Visit {API_HOST}/client/ , your game should be the last one of the list. Press on correspondant "Watch" button to see your game')
input('Press enter when ready')

# Rock and roll!
#send_move_response(game.player.ask_move(game))
start_game()

def display_board(board_data: list):
    for x in board_data:
        for y in x:
            print(y, end='')
        print()
    print()
    for x in range(len(board_data)):
        print(x, end='')
    print()



for m in c:
    if m.event == 'ask_move':

        print()
        print("Move requested")
        #game = create_game2('X', 'O', json.loads(m.data)['payload']['board'])
        try:
            print(m.data)
            my_game.current_player = 1
            my_game.board.data = json.loads(m.data)['payload']['board']
            display_board(board_data=my_game.board.data)

            print("current sign", my_game.player.filler)
            # Test here
            #send_move_response(int(input('>')))
            send_move_response(my_game.player.ask_move(my_game))

        except JSONDecodeError as e:
            logging.warning(f'wrong json: {m.data}')


    elif m.event == 'game_over':
        print("THE END?")
        exit(0)




