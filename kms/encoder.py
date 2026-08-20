from __future__ import annotations

import fcntl
from typing import TYPE_CHECKING

import kms
import kms.uapi

if TYPE_CHECKING:
    from kms import Card

__all__ = [ 'Encoder', ]

class Encoder(kms.DrmObject):
    def __init__(self, card: Card, id, idx) -> None:
        super().__init__(card, id, kms.uapi.DRM_MODE_OBJECT_ENCODER, idx)

        res = kms.uapi.drm_mode_get_encoder()

        res.encoder_id = id

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_GETENCODER, res, True)

        self.encoder_res = res

        #print(f"encoder {id}: type: {res.encoder_type}")

    def __repr__(self) -> str:
        return f'Encoder({self.id})'

    @property
    def crtc(self):
        if self.encoder_res.crtc_id:
            return self.card.get_crtc(self.encoder_res.crtc_id)

        return None

    @property
    def possible_crtcs(self):
        return [crtc for crtc in self.card.crtcs if self.encoder_res.possible_crtcs & (1 << crtc.idx)]

    @property
    def encoder_type(self):
        return kms.EncoderType(self.encoder_res.encoder_type)
