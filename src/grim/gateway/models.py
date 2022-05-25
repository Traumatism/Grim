import pydantic

from typing import Optional, Dict


class Payload(pydantic.BaseModel):
    op: int
    d: Optional[Dict]
    t: Optional[str]
    s: Optional[int]
