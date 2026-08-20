from __future__ import annotations

import ctypes
import fcntl
import weakref
from typing import TYPE_CHECKING

import kms
import kms.uapi

if TYPE_CHECKING:
    from kms import Card

__all__ = ['Blob']


class Blob(kms.DrmObject):
    def __init__(self, card: Card, data) -> None:
        blob = kms.uapi.drm_mode_create_blob()
        blob.data = ctypes.addressof(data)
        blob.length = ctypes.sizeof(data)

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_CREATEPROPBLOB, blob, True)

        super().__init__(card, blob.blob_id, kms.uapi.DRM_MODE_OBJECT_BLOB, -1)

        weakref.finalize(self, Blob.cleanup, self.card, self.id)

    @staticmethod
    def cleanup(card, id):
        blob = kms.uapi.drm_mode_destroy_blob()
        blob.blob_id = id
        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_DESTROYPROPBLOB, blob, True)

    def __repr__(self) -> str:
        return f'Blob({self.id})'
