import requests

from typing import Dict


API_URL = "https://discordapp.com/api/v6"


class Client:
    """Discord API client"""

    def __init__(self, token: str) -> None:
        self.token = token

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bot {self.token}"}

    def get(self, endpoint: str, params: Dict) -> Dict:
        """GET request"""
        return requests.get(
            f"{API_URL}/{endpoint}", params=params, headers=self.headers
        ).json()

    def post(self, endpoint: str, data: Dict) -> Dict:
        """POST request"""
        return requests.post(
            f"{API_URL}/{endpoint}", json=data, headers=self.headers
        ).json()

    def send_message(self, channel_id: int, content: str) -> Dict:
        """Send a message"""
        return self.post(
            f"channels/{channel_id}/messages",
            {"content": content},
        )
