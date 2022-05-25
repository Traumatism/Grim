import websocket
import json

from .models import Payload

from typing import Dict, Generator


class WebSocket(websocket.WebSocket):
    """Custom websocket to facilitate sending and receiving JSON"""

    def recv_json(self) -> Dict:
        """Receive a JSON object from the server"""
        return (
            {} if (response := self.recv()) is None else json.loads(response)
        )

    def send_json(self, data: Dict) -> None:
        """Send a JSON object to the server"""
        self.send(json.dumps(data))


class Gateway:
    """Discord gateway"""

    def __init__(self, token: str) -> None:
        self.ws = WebSocket()
        self.token = token

        self.session_id = 0
        self.sequence = 0

        self.connected = False

    def connect(self) -> None:

        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        self.ws.send_json(
            {
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
        )

        self.connected = True

    def listen(self) -> Generator[Payload, None, None]:
        """Listen for events"""

        # weird way to re-connect to the WS, gotta fix this ASAP

        while True:

            if self.connected is False:
                self.connect()

            try:
                data = self.ws.recv_json()
            except websocket._exceptions.WebSocketConnectionClosedException:
                self.connected = False

                resume = {
                    "op": 6,
                    "d": {
                        "token": self.token,
                        "session_id": self.session_id,
                        "seq": self.sequence,
                    },
                }

                self.ws.connect("wss://gateway.discord.gg/?v=9&encording=json")
                self.ws.send_json(resume)

                continue

            except json.decoder.JSONDecodeError:
                continue

            payload = Payload(**data)

            if payload.op != 0:
                continue

            if payload.s is not None:
                self.sequence = payload.s

            if payload.d is not None:
                self.session_id = payload.d.get("session_id", self.session_id)

            yield payload
