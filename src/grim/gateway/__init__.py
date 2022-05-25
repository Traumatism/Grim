import websocket
import time
import json

from .models import Payload

from threadz import threadify
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
        self.interval = 0

    @threadify
    def heartbeat(self) -> None:
        """Send a heartbeat"""
        while True:
            time.sleep(self.interval)

            payload = Payload(
                op=1,
                d=None,
                t=None,
                s=None,
            )

            self.ws.send_json(payload.dict())

    def connect(self) -> None:

        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        payload = Payload(
            op=2,
            d={
                "token": self.token,
                "properties": {
                    "os": "linux",
                    "browser": "chrome",
                    "device": "chrome",
                },
            },
            t=None,
            s=None,
        )

        self.ws.send_json(payload.dict())

        data = Payload(**self.ws.recv_json())

        self.interval = (data.d or {}).get("heartbeat_interval", 60000) / 1000

    def listen(self) -> Generator[Payload, None, None]:
        """Listen for events"""

        self.connect()
        self.heartbeat()

        while True:

            try:
                data = self.ws.recv_json()
            except websocket._exceptions.WebSocketConnectionClosedException:
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
