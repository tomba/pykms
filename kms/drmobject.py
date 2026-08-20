from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kms import Card

__all__ = ['DrmObject']


class DrmObject:
    def __init__(self, card: Card, id: int, type, idx: int) -> None:
        self.card = card
        self.id = id
        self.type = type
        self.idx = idx
