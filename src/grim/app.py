from .ws import WebSocket
from .client import Client
from .models import Event, Message

from rich.console import Console

from typing import Callable, TypeVar, Dict

T = TypeVar("T")


class App:
    """Main app"""

    def __init__(self, token: str, prefix: str = ".") -> None:
        super().__init__()

        self.client = Client(token)
        self.console = Console()
        self.ws = WebSocket()

        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        self.token = token
        self.prefix = prefix

        self.__listeners: Dict[str, Callable[[Message], str]] = {}

    def command(
        self, func: Callable[[Message], str]
    ) -> Callable[[Message], str]:
        """Decorator to add a new command"""

        def wrapper(message: Message) -> str:

            self.console.log(
                f"handling command {message.content}",
                f"from {message.author.full_name}",
            )

            return func(message)

        self.__listeners[f"{self.prefix}{func.__name__}"] = wrapper

        return wrapper

    def not_found(self, message: Message) -> str:
        """Return a message if the command is not found"""
        return f"Command `{message.content}` not found"

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

        self.console.log("listening for messages....")

        while True:

            try:
                event = Event(**self.ws.recv_json())
            except Exception:
                continue

            if event.t == "MESSAGE_CREATE":

                message = Message(**event.d)

                if (
                    not message.content.startswith(self.prefix)
                    or message.author.id == self.client.user.id
                ):
                    continue

                answer = self.__listeners.get(
                    message.command or "", self.not_found
                )(message)

                self.client.send_message(message.channel_id, answer)
