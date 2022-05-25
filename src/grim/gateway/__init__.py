import contextlib
import websocket
import json

from .models import Payload

from typing import Dict, Generator


class WebSocket(websocket.WebSocket):
    """Custom websocket to facilitate sending and receiving JSON"""

    def recv_json(self) -> Dict:
        """Receive a JSON object from the server"""
        response = self.recv()

        if response is None:
            return {}

        return json.loads(response)

    def send_json(self, data: Dict) -> None:
        """Send a JSON object to the server"""
        self.send(json.dumps(data))


class Gateway:
    """Discord gateway"""

    def __init__(self, token: str) -> None:
        self.ws = WebSocket()
        self.token = token

        self.connected = False

    def connect(self) -> None:
        self.connected = True

        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "linux",
                    "$browser": "chrome",
                    "$device": "pc",
                },
            },
        }

        self.ws.send_json(payload)

    def listen(self) -> Generator[Payload, None, None]:
        """Listen for events"""

        if self.connected is False:
            self.connect()

        # weird way to re-connect to the WS, gotta fix this ASAP
        while True:
            try:
                data = self.ws.recv_json()
            except websocket._exceptions.WebSocketConnectionClosedException:
                self.connected = False
                self.connect()
                continue

            with contextlib.suppress(json.decoder.JSONDecodeError):
                yield Payload(**data)
