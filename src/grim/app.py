from .ws import WebSocket
from .client import Client
from .models import Event, Message

from rich.console import Console

from typing import Callable, Iterable, Tuple, TypeVar, Dict

T = TypeVar("T")


class App:
    """Main app"""

    def __init__(self, token: str, prefix: str = ".") -> None:
        super().__init__()

        self.ws = WebSocket()
        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")

        self.console = Console()

        self.client = Client(token)

        self.prefix = prefix

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

            self.console.log(
                f"handling command {message.content}",
                f"from {message.author.full_name}",
            )

            return func(message)

        self.__listeners[f"{self.prefix}{func.__name__}"] = wrapper

        return wrapper

    def parse_content(self, content: str) -> Tuple[str, Iterable[str]]:
        """Parse the content"""
        parts = content.split(" ")

        if len(parts) == 1:
            return parts[0], []

        return parts[0], parts[1:]

    def not_found(self, message: Message) -> str:
        """Return a message if the command is not found"""
        return f"command {message.content} not found"

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

                command, _ = self.parse_content(message.content)

                answer = self.__listeners.get(command, self.not_found)(message)

                self.client.send_message(message.channel_id, answer)
