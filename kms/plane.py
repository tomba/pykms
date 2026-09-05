from __future__ import annotations

import ctypes
import fcntl
from typing import TYPE_CHECKING

import kms
import kms.uapi
from kms.drmpropobject import DrmPropObject

if TYPE_CHECKING:
    from kms import Card, Crtc

__all__ = [
    'Plane',
]


class Plane(DrmPropObject):
    def __init__(self, card: Card, id, idx) -> None:
        super().__init__(card, id, kms.uapi.DRM_MODE_OBJECT_PLANE, idx)

        plane = kms.uapi.drm_mode_get_plane()

        plane.plane_id = id

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_GETPLANE, plane, True)

        format_types = (kms.uapi.c_uint32 * plane.count_format_types)()
        plane.format_type_ptr = ctypes.addressof(format_types)

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_GETPLANE, plane, True)

        formats = []
        for fourcc in format_types:
            try:
                format = kms.PixelFormats.find_drm_fourcc(fourcc)
            except StopIteration:
                continue

            formats.append(format)

        self.format_types = formats
        self.res = plane

        # print(f"plane {id}: fb: {plane.fb_id}")

    def __repr__(self) -> str:
        return f'Plane({self.id})'

    def supports_crtc(self, crtc: Crtc):
        return bool(self.res.possible_crtcs & (1 << crtc.idx))

    @property
    def plane_type(self):
        return kms.PlaneType(self.get_prop_value('type'))

    def supports_format(self, format: kms.PixelFormat):
        return format in self.format_types

    @property
    def crtc_id(self):
        return self.res.crtc_id

    @property
    def fb_id(self):
        return self.res.fb_id
