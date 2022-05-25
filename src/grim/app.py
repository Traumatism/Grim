from .gateway import Gateway
from .client import Client
from .models import Message

from rich.console import Console

from threadz import threadify
from typing import Callable, Optional, TypeVar, Dict, Generator


T = TypeVar("T")

CommandCallable = Callable[[Message], Generator[str, None, None]]


class App:
    """Main app"""

    def __init__(
        self,
        token: str,
        prefix: Optional[str] = None,
    ) -> None:

        self.client = Client(token)
        self.console = Console()
        self.gateway = Gateway(token)

        self.token = token
        self.prefix = prefix or ""

        self.__listeners: Dict[str, CommandCallable] = {}

    def command(self, func: CommandCallable) -> CommandCallable:
        """Decorator to add a new command"""

        def wrapper(message: Message) -> Generator[str, None, None]:

            self.console.log(
                f"handling command {message.content}",
                f"from {message.author.full_name}",
            )

            return func(message)

        self.__listeners[f"{self.prefix}{func.__name__}"] = wrapper

        return wrapper

    @threadify
    def run_command(self, func: CommandCallable, message: Message):
        """Run a command"""
        for content in func(message):
            self.client.send_message(message.channel_id, content)

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

                func = self.__listeners.get(message.command or "")

                if func is None:
                    continue

                self.run_command(func, message)
