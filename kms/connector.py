from __future__ import annotations

import ctypes
import fcntl
from typing import TYPE_CHECKING, ClassVar

import kms
import kms.uapi
from kms.drmpropobject import DrmPropObject

if TYPE_CHECKING:
    from kms import Card

__all__ = [
    'Connector',
]


class Connector(DrmPropObject):
    connector_names: ClassVar[dict[int, str]] = {
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
        kms.uapi.DRM_MODE_CONNECTOR_WRITEBACK: 'Writeback',
        kms.uapi.DRM_MODE_CONNECTOR_SPI: 'SPI',
        kms.uapi.DRM_MODE_CONNECTOR_USB: 'USB',
    }

    def __init__(self, card: Card, id, idx) -> None:
        super().__init__(card, id, kms.uapi.DRM_MODE_OBJECT_CONNECTOR, idx)

        self._read_connector()

        res = self.connector_res

        type_name = Connector.connector_names.get(
            res.connector_type, f'Unknown{res.connector_type}'
        )
        self.fullname = f'{type_name}-{res.connector_type_id}'

    def _read_connector(self):
        res = kms.uapi.drm_mode_get_connector(connector_id=self.id)

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_GETCONNECTOR, res, True)

        encoder_ids = (kms.uapi.c_uint32 * res.count_encoders)()
        res.encoders_ptr = ctypes.addressof(encoder_ids)

        modes = (kms.uapi.drm_mode_modeinfo * res.count_modes)()
        res.modes_ptr = ctypes.addressof(modes)

        # The properties are fetched by DrmPropObject.refresh_props()
        res.count_props = 0

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_GETCONNECTOR, res, True)

        self.connector_res = res
        self.encoder_ids = encoder_ids
        self.modes = [kms.VideoMode._from_modeinfo(m) for m in modes]

    def refresh(self):
        """Re-read the connector state (connection status, modes, encoders)
        and the properties from the kernel."""
        self._read_connector()
        self.refresh_props()

    @property
    def connected(self):
        return self.connector_res.connection in (
            kms.uapi.DRM_MODE_CONNECTED,
            kms.uapi.DRM_MODE_UNKNOWNCONNECTION,
        )

    def refresh_modes(self):
        """Deprecated, use refresh()."""
        self.refresh()

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
