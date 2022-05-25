from .gateway import Gateway
from .client import Client
from .models import Message

from rich.console import Console

from typing import Callable, Optional, TypeVar, Dict

T = TypeVar("T")


class App:
    """Main app"""

    def __init__(self, token: str, prefix: Optional[str] = None) -> None:
        super().__init__()

        self.client = Client(token)
        self.console = Console()
        self.gateway = Gateway(token)

        self.token = token
        self.prefix = prefix or ""

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
        self.console.log("listening for messages....")

        for event in self.gateway.listen():
            if event.d is None:
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
