from __future__ import annotations

import ctypes
import fcntl
from typing import TYPE_CHECKING

import kms
import kms.uapi
from kms.drmobject import DrmObject

if TYPE_CHECKING:
    from kms import Card

__all__ = [
    'DrmPropObject',
]


class DrmPropObject(DrmObject):
    def __init__(self, card: Card, id, type, idx) -> None:
        super().__init__(card, id, type, idx)
        self.refresh_props()

    def refresh_props(self):
        props = kms.uapi.drm_mode_obj_get_properties()
        props.obj_id = self.id
        props.obj_type = self.type

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_OBJ_GETPROPERTIES, props, True)

        prop_ids = (kms.uapi.c_uint32 * props.count_props)()
        props.props_ptr = ctypes.addressof(prop_ids)

        prop_values = (kms.uapi.c_uint64 * props.count_props)()
        props.prop_values_ptr = ctypes.addressof(prop_values)

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_OBJ_GETPROPERTIES, props, True)

        self.prop_values = {int(prop_ids[i]): int(prop_values[i]) for i in range(props.count_props)}

    def get_prop_value(self, prop_name: str):
        prop_id = self.card.find_property_id(self, prop_name)
        assert prop_id in self.prop_values
        return self.prop_values[prop_id]

    def set_prop(self, prop, value):
        areq = kms.atomicreq.AtomicReq(self.card)
        areq.add(self, prop, value)
        areq.commit_sync()

    def set_props(self, map):
        areq = kms.atomicreq.AtomicReq(self.card)
        areq.add_many(self, map)
        areq.commit_sync()

    @property
    def props(self):
        l = []
        for pid, val in self.prop_values.items():
            prop = self.card.find_property(pid)
            l.append((prop, prop.conv_raw_to_val(val)))
        return l
