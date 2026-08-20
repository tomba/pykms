from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from kms import Framebuffer


class RGB:
    def __init__(self, a, r, g, b):
        self.a = a
        self.r = r
        self.b = b
        self.g = g

    def to_rgba(self):
        return (self.b << 0) | (self.g << 8) | (self.r << 16) | (self.a << 24)


class NumpyFramebuffer:
    def __init__(self, fb: Framebuffer, prepopulate=False):
        map = fb.map(0)
        self.b = np.frombuffer(map, dtype=np.int32).reshape(fb.height, fb.width)

        # Is there a better way to populate page tables
        if prepopulate:
            self.b[:, :] = 0

    def fill_rect(self, x, y, w, h, c):
        if isinstance(c, RGB):
            c = c.to_rgba()

        self.b[y : y + h, x : x + w] = c

    def draw_gradient(self, x, y, h, gradient):
        self.b[y : y + h, x : x + len(gradient)] = gradient

    def draw_color_bar(self, old_xpos, new_xpos, bar_width):
        self.b[:, old_xpos : old_xpos + bar_width] = 0
        self.b[:, new_xpos : new_xpos + bar_width] = 0xFFFFFF
