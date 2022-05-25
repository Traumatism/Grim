from typing import Optional


def italic(text: str) -> str:
    """Italic text"""
    return f"*{text}*"


def bold(text: str) -> str:
    """Bold text"""
    return f"**{text}**"


def underline(text: str) -> str:
    """Underline text"""
    return f"__{text}__"


def strikethrough(text: str) -> str:
    """Strike through text"""
    return f"~~{text}~~"


def code(text: str) -> str:
    """Build a code text"""
    return f"`{text}`"


def code_block(text: str, lang: Optional[str] = None) -> str:
    """Build a code block"""
    return f"```{text}```" if lang is None else f"```{lang}\n{text}```"
