import pydantic

from typing import Dict, List, Optional


class Event(pydantic.BaseModel):
    t: Optional[str]
    d: Dict


class User(pydantic.BaseModel):
    id: int
    username: str
    discriminator: str

    @property
    def full_name(self) -> str:
        return f"{self.username}#{self.discriminator}"


class Message(pydantic.BaseModel):
    id: int
    guild_id: int
    channel_id: int
    type: int
    timestamp: str
    content: str
    author: User

    @property
    def arguments(self) -> List[str]:
        parts = self.content.split()

        return [] if len(parts) == 1 else parts[1:]

    @property
    def command(self) -> Optional[str]:
        parts = self.content.split()

        return None if len(parts) == 0 else parts[0]
