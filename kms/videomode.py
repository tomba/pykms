from __future__ import annotations

from enum import IntFlag
from typing import TYPE_CHECKING

import kms.uapi

if TYPE_CHECKING:
    from kms import Card

__all__ = ['VideoMode', 'ModeFlag', 'ModeType']


class ModeFlag(IntFlag):
    HSYNC_POS = kms.uapi.DRM_MODE_FLAG_PHSYNC
    HSYNC_NEG = kms.uapi.DRM_MODE_FLAG_NHSYNC
    VSYNC_POS = kms.uapi.DRM_MODE_FLAG_PVSYNC
    VSYNC_NEG = kms.uapi.DRM_MODE_FLAG_NVSYNC
    INTERLACE = kms.uapi.DRM_MODE_FLAG_INTERLACE
    DBLSCAN = kms.uapi.DRM_MODE_FLAG_DBLSCAN
    CSYNC = kms.uapi.DRM_MODE_FLAG_CSYNC
    CSYNC_POS = kms.uapi.DRM_MODE_FLAG_PCSYNC
    CSYNC_NEG = kms.uapi.DRM_MODE_FLAG_NCSYNC
    HSKEW = kms.uapi.DRM_MODE_FLAG_HSKEW
    DBLCLK = kms.uapi.DRM_MODE_FLAG_DBLCLK
    CLKDIV2 = kms.uapi.DRM_MODE_FLAG_CLKDIV2


class ModeType(IntFlag):
    BUILTIN = kms.uapi.DRM_MODE_TYPE_BUILTIN
    PREFERRED = kms.uapi.DRM_MODE_TYPE_PREFERRED
    DEFAULT = kms.uapi.DRM_MODE_TYPE_DEFAULT
    USERDEF = kms.uapi.DRM_MODE_TYPE_USERDEF
    DRIVER = kms.uapi.DRM_MODE_TYPE_DRIVER


class VideoMode:
    def __init__(self):
        self.clock: int = 0
        self.hdisplay: int = 0
        self.hfp: int = 0
        self.hsw: int = 0
        self.hbp: int = 0
        self.vdisplay: int = 0
        self.vfp: int = 0
        self.vsw: int = 0
        self.vbp: int = 0
        self.hskew: int = 0
        self.vscan: int = 0
        self.vrefresh: int = 0
        self.flags: ModeFlag = ModeFlag(0)
        self.type: ModeType = ModeType(0)
        self.name: str = ''

    @classmethod
    def _from_modeinfo(cls, modeinfo: kms.uapi.drm_mode_modeinfo) -> VideoMode:
        mode = cls()
        mode.clock = modeinfo.clock * 1000
        mode.hdisplay = modeinfo.hdisplay
        mode.hfp = modeinfo.hsync_start - modeinfo.hdisplay
        mode.hsw = modeinfo.hsync_end - modeinfo.hsync_start
        mode.hbp = modeinfo.htotal - modeinfo.hsync_end
        mode.vdisplay = modeinfo.vdisplay
        mode.vfp = modeinfo.vsync_start - modeinfo.vdisplay
        mode.vsw = modeinfo.vsync_end - modeinfo.vsync_start
        mode.vbp = modeinfo.vtotal - modeinfo.vsync_end
        mode.hskew = modeinfo.hskew
        mode.vscan = modeinfo.vscan
        mode.vrefresh = modeinfo.vrefresh
        mode.flags = ModeFlag(modeinfo.flags)
        mode.type = ModeType(modeinfo.type)
        mode.name = modeinfo.name.decode('utf-8')
        return mode

    def _to_modeinfo(self) -> kms.uapi.drm_mode_modeinfo:
        m = kms.uapi.drm_mode_modeinfo()
        m.clock = self.clock // 1000
        m.hdisplay = self.hdisplay
        m.hsync_start = self.hsync_start
        m.hsync_end = self.hsync_end
        m.htotal = self.htotal
        m.hskew = self.hskew
        m.vdisplay = self.vdisplay
        m.vsync_start = self.vsync_start
        m.vsync_end = self.vsync_end
        m.vtotal = self.vtotal
        m.vscan = self.vscan
        m.vrefresh = self.vrefresh
        m.flags = int(self.flags)
        m.type = int(self.type)
        m.name = self.name.encode('utf-8')
        return m

    def __repr__(self):
        return f'VideoMode({self.hdisplay}x{self.vdisplay})'

    def __str__(self):
        return f'{self.hdisplay}x{self.vdisplay}@{self.vrefresh}'

    def to_blob(self, card: Card):
        return kms.Blob(card, self._to_modeinfo())

    def copy(self) -> VideoMode:
        new = VideoMode()
        new.__dict__.update(self.__dict__)
        return new

    # X modeline style properties (computed, read-only)

    @property
    def hsync_start(self):
        return self.hdisplay + self.hfp

    @property
    def hsync_end(self):
        return self.hdisplay + self.hfp + self.hsw

    @property
    def htotal(self):
        return self.hdisplay + self.hfp + self.hsw + self.hbp

    @property
    def vsync_start(self):
        return self.vdisplay + self.vfp

    @property
    def vsync_end(self):
        return self.vdisplay + self.vfp + self.vsw

    @property
    def vtotal(self):
        return self.vdisplay + self.vfp + self.vsw + self.vbp

    @property
    def calculated_vrefresh(self):
        return self.clock / (self.htotal * self.vtotal)

    # Flag-based properties

    @property
    def interlace(self):
        return bool(self.flags & ModeFlag.INTERLACE)

    @property
    def hsync_polarity(self):
        """Horizontal Sync Polarity: 1 = positive, -1 = negative, 0 = not specified"""
        if self.flags & ModeFlag.HSYNC_POS:
            return 1
        elif self.flags & ModeFlag.HSYNC_NEG:
            return -1
        else:
            return 0

    @property
    def vsync_polarity(self):
        """Vertical Sync Polarity: 1 = positive, -1 = negative, 0 = not specified"""
        if self.flags & ModeFlag.VSYNC_POS:
            return 1
        elif self.flags & ModeFlag.VSYNC_NEG:
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
