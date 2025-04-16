from __future__ import annotations

from typing import TYPE_CHECKING

import kms.uapi

if TYPE_CHECKING:
    from kms import Card

__all__ = ['VideoMode']


class VideoMode:
    def __init__(self, modeinfo: kms.uapi.drm_mode_modeinfo):
        self.modeinfo = modeinfo

    def __repr__(self):
        return f'VideoMode({self.modeinfo.hdisplay}x{self.modeinfo.vdisplay})'

    def __str__(self):
        return f'{self.modeinfo.hdisplay}x{self.modeinfo.vdisplay}@{self.modeinfo.vrefresh}'

    def to_blob(self, card: Card):
        return kms.Blob(card, self.modeinfo)

    @property
    def clock(self):
        # modeinfo stores clock in kHz
        return self.modeinfo.clock * 1000

    @clock.setter
    def clock(self, value: int):
        # modeinfo expects clock in kHz
        self.modeinfo.clock = value // 1000

    # X11 style timings

    @property
    def hdisplay(self):
        return self.modeinfo.hdisplay

    @property
    def hsync_start(self):
        return self.modeinfo.hsync_start

    @property
    def hsync_end(self):
        return self.modeinfo.hsync_end

    @property
    def htotal(self):
        return self.modeinfo.htotal

    @property
    def hskew(self):
        return self.modeinfo.hskew

    @property
    def vdisplay(self):
        return self.modeinfo.vdisplay

    @property
    def vsync_start(self):
        return self.modeinfo.vsync_start

    @property
    def vsync_end(self):
        return self.modeinfo.vsync_end

    @property
    def vtotal(self):
        return self.modeinfo.vtotal

    @property
    def vscan(self):
        return self.modeinfo.vscan

    @property
    def vrefresh(self):
        return self.modeinfo.vrefresh

    @property
    def flags(self):
        return self.modeinfo.flags

    @property
    def type(self):
        return self.modeinfo.type

    @property
    def name(self):
        return self.modeinfo.name.decode('utf-8')

    # Conventional timing properties (horizontal)
    @property
    def hfp(self):
        """Horizontal Front Porch"""
        return self.hsync_start - self.hdisplay

    @property
    def hsw(self):
        """Horizontal Sync Width"""
        return self.hsync_end - self.hsync_start

    @property
    def hbp(self):
        """Horizontal Back Porch"""
        return self.htotal - self.hsync_end

    # Conventional timing properties (vertical)
    @property
    def vfp(self):
        """Vertical Front Porch"""
        return self.vsync_start - self.vdisplay

    @property
    def vsw(self):
        """Vertical Sync Width"""
        return self.vsync_end - self.vsync_start

    @property
    def vbp(self):
        """Vertical Back Porch"""
        return self.vtotal - self.vsync_end

    @property
    def calculated_vrefresh(self):
        return self.clock / (self.htotal * self.vtotal)

    # Flag-based properties
    @property
    def interlace(self):
        return self.modeinfo.flags & kms.uapi.DRM_MODE_FLAG_INTERLACE

    @property
    def hsync_polarity(self):
        """Horizontal Sync Polarity: 1 = positive, -1 = negative, 0 = not specified"""
        if self.modeinfo.flags & kms.uapi.DRM_MODE_FLAG_PHSYNC:
            return 1
        elif self.modeinfo.flags & kms.uapi.DRM_MODE_FLAG_NHSYNC:
            return -1
        else:
            return 0

    @property
    def vsync_polarity(self):
        """Vertical Sync Polarity: 1 = positive, -1 = negative, 0 = not specified"""
        if self.modeinfo.flags & kms.uapi.DRM_MODE_FLAG_PVSYNC:
            return 1
        elif self.modeinfo.flags & kms.uapi.DRM_MODE_FLAG_NVSYNC:
            return -1
        else:
            return 0

    def to_str_modeline(self):
        return (
            f'{self.hdisplay}x{self.vdisplay}@{self.calculated_vrefresh:.2f} '
            f'{self.clock} Hz '
            f'H: {self.hdisplay}/{self.hsync_start}/{self.hsync_end}/{self.htotal} '
            f'V: {self.vdisplay}/{self.vsync_start}/{self.vsync_end}/{self.vtotal}'
        )

    def to_str(self):
        return (
            f'{self.hdisplay}x{self.vdisplay}@{self.calculated_vrefresh:.2f}'
            f'{"i" if self.interlace else ""} '
            f'{self.clock} Hz '
            f'{self.hdisplay}/{self.hfp}/{self.hsw}/{self.hbp}/{self.htotal}/{["-", "?", "+"][self.hsync_polarity + 1]} '
            f'{self.vdisplay}/{self.vfp}/{self.vsw}/{self.vbp}/{self.vtotal}/{["-", "?", "+"][self.vsync_polarity + 1]}'
        )
