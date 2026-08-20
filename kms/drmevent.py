from __future__ import annotations

from enum import Enum, auto

__all__ = ['DrmEvent', 'DrmEventType']


class DrmEventType(Enum):
    FLIP_COMPLETE = auto()


class DrmEvent:
    def __init__(self, type, seq, time, data):
        self.type = type
        self.seq = seq
        self.time = time
        self.data = data
