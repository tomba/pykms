from __future__ import annotations

import ctypes
import fcntl
from enum import Enum, auto
from typing import TYPE_CHECKING

import kms
import kms.uapi
from kms.drmobject import DrmObject

if TYPE_CHECKING:
    from kms import Card

__all__ = ['DrmProperty', 'DrmPropertyType']


class DrmPropertyType(Enum):
    RANGE = auto()
    ENUM = auto()
    BLOB = auto()
    BITMASK = auto()
    OBJECT = auto()
    SIGNED_RANGE = auto()


class DrmProperty(DrmObject):
    def __init__(self, card: Card, id) -> None:
        super().__init__(card, id, kms.uapi.DRM_MODE_OBJECT_PROPERTY, -1)

        prop = kms.uapi.drm_mode_get_property(prop_id=id)
        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_GETPROPERTY, prop, True)

        self.name = prop.name.decode('ascii')

        self.immutable = prop.flags & kms.uapi.DRM_MODE_PROP_IMMUTABLE
        self.atomic = prop.flags & kms.uapi.DRM_MODE_PROP_ATOMIC

        ext_type = prop.flags & kms.uapi.DRM_MODE_PROP_EXTENDED_TYPE

        if prop.flags & kms.uapi.DRM_MODE_PROP_RANGE:
            self.type = DrmPropertyType.RANGE
        elif prop.flags & kms.uapi.DRM_MODE_PROP_ENUM:
            self.type = DrmPropertyType.ENUM
        elif prop.flags & kms.uapi.DRM_MODE_PROP_BLOB:
            self.type = DrmPropertyType.BLOB
        elif prop.flags & kms.uapi.DRM_MODE_PROP_BITMASK:
            self.type = DrmPropertyType.BITMASK
        elif ext_type == kms.uapi.DRM_MODE_PROP_OBJECT:
            self.type = DrmPropertyType.OBJECT
        elif ext_type == kms.uapi.DRM_MODE_PROP_SIGNED_RANGE:
            self.type = DrmPropertyType.SIGNED_RANGE
        else:
            raise NotImplementedError()

        if prop.count_values > 0:
            prop_values = (kms.uapi.c_uint64 * prop.count_values)()
            prop.values_ptr = ctypes.addressof(prop_values)
        else:
            prop_values = []

        if self.type in (DrmPropertyType.ENUM, DrmPropertyType.BITMASK):
            enum_blobs = (kms.uapi.drm_mode_property_enum * prop.count_enum_blobs)()
            prop.enum_blob_ptr = ctypes.addressof(enum_blobs)
        else:
            enum_blobs = []

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_GETPROPERTY, prop, True)

        self.values = [self.conv_raw_to_val(v) for v in prop_values]

        self.enum_descs = [(e.value, e.name.decode('ascii')) for e in enum_blobs]

    def conv_raw_to_val(self, v):
        return ctypes.c_int64(v).value if self.type == DrmPropertyType.SIGNED_RANGE else v
