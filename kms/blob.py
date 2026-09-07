from __future__ import annotations

import ctypes
import fcntl
import weakref
from typing import TYPE_CHECKING

import kms
import kms.uapi
from kms.drmobject import DrmObject

if TYPE_CHECKING:
    from kms import Card

__all__ = ['Blob']


class Blob(DrmObject):
    """A kernel property blob, e.g. a mode for the CRTC MODE_ID property.

    The Blob object owns the kernel blob: the blob is destroyed when the
    object is garbage collected. Requests only store the blob ID, so keep a
    reference to the Blob until every commit that uses it has returned.
    Passing a temporary such as ``mode.to_blob(card)`` directly to
    :meth:`AtomicReq.add_crtc` destroys the blob before the commit, which
    then fails with EINVAL. After a successful commit the kernel holds its
    own reference for as long as the blob is in use, so the object may be
    dropped then.
    """

    def __init__(self, card: Card, data) -> None:
        """Create a property blob from a ctypes object or a bytes-like object.
        The kernel copies the data, so the data object need not stay alive
        after this. The Blob object itself must; see the class docstring."""
        if isinstance(data, (bytes, bytearray, memoryview)):
            mv = memoryview(data).cast('B')
            data = (ctypes.c_ubyte * mv.nbytes).from_buffer_copy(mv)

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
