import requests
from sseclient import SSEClient

from core import create_game


class GameWrapper:

    def __init__(self, api_host: str, player_name: str):
        payload = {
            "creator_name": player_name,
            "session_name": "Unnamed Session",
            "board_w": 8,
            "board_h": 8
        }
        print("Creating game. This may take a while...")

        raw = requests.put(f'{api_host}/game/d_ai_battle', json=payload)
        rsp = raw.json()

        my_game = create_game(rsp)
        print('Done')
        session_id, watch_id, listener_id = rsp['session_id'], rsp['stream'], rsp['notifications']

        self.game = my_game
        self.watch_id = watch_id
        self.api_host = api_host
        self.session_id = session_id
        self.listener_id = listener_id

    def send_move_response(self, response: int):

        print("Selected move", response)

        move_payload = {
            "type": "ask_move_rs",
            "payload": {'pos': response, 'sender_id': self.watch_id}
        }

        url = f'{self.api_host}/game/dispatch/{self.session_id}/{self.listener_id}'
        requests.post(url, json=move_payload)

    def start(self) -> SSEClient:

        move_payload = {
            "type": "ask_move",
            "payload": {'sender_id': self.watch_id, 'payload': {'board': self.game.board.data}}
        }

        url = f'{self.api_host}/game/dispatch/{self.session_id}/{self.watch_id}'
        requests.post(url, json=move_payload)
        client = SSEClient(f'{self.api_host}/game/stream/{self.session_id}/{self.watch_id}')
        client.chunk_size = 512
        return client

    def end(self):

        requests.delete(f'{self.api_host}/session/{self.session_id}')

    def display_board(self):
        for x in self.game.board.data:
            for y in x:
                print(y, end='')
            print()
        print()
        for x in range(len(self.game.board.data)):
            print(x, end='')
        print()



