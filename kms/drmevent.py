from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

__all__ = ['DrmEvent', 'DrmEventType']


class DrmEventType(Enum):
    VBLANK = auto()
    FLIP_COMPLETE = auto()
    CRTC_SEQUENCE = auto()


@dataclass
class DrmEvent:
    type: DrmEventType
    seq: int
    time: float
    data: int
    crtc_id: int = 0
