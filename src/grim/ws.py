import websocket
import json

from typing import Dict


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
