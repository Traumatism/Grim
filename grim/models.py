import pydantic

from typing import Dict


class Event(pydantic.BaseModel):
    t: str
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
