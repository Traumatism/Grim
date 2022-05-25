from .ws import WebSocket
from .client import Client
from .models import Event, Message

from rich.console import Console

from typing import Callable, TypeVar, Dict

T = TypeVar("T")


class App:
    """Main app"""

    def __init__(self, token: str) -> None:
        super().__init__()

        self.ws = WebSocket()
        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        self.console = Console()

        self.client = Client(token)

        self.__token = token
        self.__listeners: Dict[str, Callable[[Message], str]] = {}

    @property
    def token(self) -> str:
        """Warning: access this property only if you know what you are doing"""
        return self.__token

    def command(
        self, func: Callable[[Message], str]
    ) -> Callable[[Message], str]:
        """Decorator to add a new command"""

        def wrapper(message: Message) -> str:
            return func(message)

        self.__listeners[func.__name__] = wrapper

        return wrapper

    def listen(self):
        """Listen for messages"""

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

        while True:

            try:
                event = Event(**self.ws.recv_json())
            except Exception:
                continue

            if event.t == "MESSAGE_CREATE":

                message = Message(**event.d)

                if message.author.id == self.client.user.id:
                    continue

                for listener in self.__listeners.values():
                    answer = listener(message)

                    self.client.send_message(message.channel_id, answer)
