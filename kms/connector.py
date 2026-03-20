from __future__ import annotations

import ctypes
import fcntl

from typing import TYPE_CHECKING

import kms
import kms.uapi

if TYPE_CHECKING:
    from kms import Card

__all__ = [ 'Connector', ]

class Connector(kms.DrmPropObject):
    connector_names = {
        kms.uapi.DRM_MODE_CONNECTOR_Unknown: 'Unknown',
        kms.uapi.DRM_MODE_CONNECTOR_VGA: 'VGA',
        kms.uapi.DRM_MODE_CONNECTOR_DVII: 'DVI-I',
        kms.uapi.DRM_MODE_CONNECTOR_DVID: 'DVI-D',
        kms.uapi.DRM_MODE_CONNECTOR_DVIA: 'DVI-A',
        kms.uapi.DRM_MODE_CONNECTOR_Composite: 'Composite',
        kms.uapi.DRM_MODE_CONNECTOR_SVIDEO: 'S-Video',
        kms.uapi.DRM_MODE_CONNECTOR_LVDS: 'LVDS',
        kms.uapi.DRM_MODE_CONNECTOR_Component: 'Component',
        kms.uapi.DRM_MODE_CONNECTOR_9PinDIN: '9-Pin-DIN',
        kms.uapi.DRM_MODE_CONNECTOR_DisplayPort: 'DP',
        kms.uapi.DRM_MODE_CONNECTOR_HDMIA: 'HDMI-A',
        kms.uapi.DRM_MODE_CONNECTOR_HDMIB: 'HDMI-B',
        kms.uapi.DRM_MODE_CONNECTOR_TV: 'TV',
        kms.uapi.DRM_MODE_CONNECTOR_eDP: 'eDP',
        kms.uapi.DRM_MODE_CONNECTOR_VIRTUAL: 'Virtual',
        kms.uapi.DRM_MODE_CONNECTOR_DSI: 'DSI',
        kms.uapi.DRM_MODE_CONNECTOR_DPI: 'DPI',
    }

    def __init__(self, card: Card, id, idx) -> None:
        super().__init__(card, id, kms.uapi.DRM_MODE_OBJECT_CONNECTOR, idx)

        res = kms.uapi.drm_mode_get_connector(connector_id=id)

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_GETCONNECTOR, res, True)

        encoder_ids = (kms.uapi.c_uint32 * res.count_encoders)()
        res.encoders_ptr = ctypes.addressof(encoder_ids)

        modes = (kms.uapi.drm_mode_modeinfo * res.count_modes)()
        res.modes_ptr = ctypes.addressof(modes)

        prop_ids = (kms.uapi.c_uint32 * res.count_props)()
        res.props_ptr = ctypes.addressof(prop_ids)

        prop_values = (kms.uapi.c_uint64 * res.count_props)()
        res.prop_values_ptr = ctypes.addressof(prop_values)

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_GETCONNECTOR, res, True)

        self.connector_res = res
        self.encoder_ids = encoder_ids
        self.modes = [kms.VideoMode._from_modeinfo(m) for m in modes]

        self.fullname = f'{Connector.connector_names[res.connector_type]}-{res.connector_type_id}'

        #print(f"connector {id}: type: {res.connector_type}, num_modes: {len(self.modes)}")

    @property
    def connected(self):
        return self.connector_res.connection in (kms.uapi.DRM_MODE_CONNECTED, kms.uapi.DRM_MODE_UNKNOWNCONNECTION)

    def refresh_modes(self):
        res = kms.uapi.drm_mode_get_connector(connector_id=self.id)

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_GETCONNECTOR, res, True)

        modes = (kms.uapi.drm_mode_modeinfo * res.count_modes)()
        res.modes_ptr = ctypes.addressof(modes)

        res.count_props = 0
        res.count_encoders = 0

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_GETCONNECTOR, res, True)

        self.modes = [kms.VideoMode._from_modeinfo(m) for m in modes]

    def get_default_mode(self):
        return self.modes[0]

    def get_mode(self, name: str):
        raise NotImplementedError()

    @property
    def current_crtc(self):
        if self.connector_res.encoder_id == 0:
            return None
        enc = self.card.get_encoder(self.connector_res.encoder_id)
        return enc.crtc

    def __repr__(self) -> str:
        return f'Connector({self.id})'

    def __str__(self) -> str:
        return f'{self.fullname}({self.id})'

    @property
    def possible_crtcs(self):
        crtcs = set()

        for encoder_id in self.encoder_ids:
            crtcs.update(self.card.get_encoder(encoder_id).possible_crtcs)

        return crtcs

    @property
    def encoders(self):
        return [self.card.get_encoder(eid) for eid in self.encoder_ids]
