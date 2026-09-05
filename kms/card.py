from __future__ import annotations

import ctypes
import fcntl
import glob
import io
import os
import weakref
from dataclasses import dataclass

import kms.uapi
from kms.connector import Connector
from kms.crtc import Crtc
from kms.drmevent import DrmEvent, DrmEventType
from kms.drmobject import DrmObject
from kms.drmproperty import DrmProperty
from kms.drmpropobject import DrmPropObject
from kms.encoder import Encoder
from kms.framebuffer import Framebuffer
from kms.plane import Plane

__all__ = [
    'Card',
    'Version',
]


@dataclass
class Version:
    major: int
    minor: int
    patchlevel: int
    name: str
    date: str
    desc: str


class Card:
    def __init__(self, dev_path: str | None = None) -> None:
        if not dev_path:
            dev_path = Card.__open_first_kms_device()

        self.dev_path = dev_path

        self.fio = io.FileIO(
            dev_path, opener=lambda name, _: os.open(name, os.O_RDWR | os.O_NONBLOCK)
        )

        self.set_defaults()
        self.get_res()
        self.get_plane_res()
        self.collect_props()

        self.event_buf = bytearray(1024)

        weakref.finalize(self, self.fio.close)

    @staticmethod
    def __open_first_kms_device() -> str:
        for path in sorted(glob.glob('/dev/dri/card*')):
            try:
                fd = os.open(path, os.O_RDWR | os.O_NONBLOCK)
            except OSError:
                continue

            try:
                res = kms.uapi.drm_mode_card_res()
                fcntl.ioctl(fd, kms.uapi.DRM_IOCTL_MODE_GETRESOURCES, res, True)

                if res.count_crtcs > 0 and res.count_connectors > 0 and res.count_encoders > 0:
                    return path
            except OSError:
                pass
            finally:
                os.close(fd)

        raise FileNotFoundError('No KMS capable card found')

    @property
    def fd(self):
        return self.fio.fileno()

    def collect_props(self):
        prop_ids = set()

        for ob in [*self.crtcs, *self.connectors, *self.planes]:
            for prop_id in ob.prop_values:
                prop_ids.add(prop_id)

        props = {}

        for prop_id in prop_ids:
            prop = DrmProperty(self, prop_id)
            props[prop_id] = prop

        self._props: dict[int, DrmProperty] = props

    def find_property(self, prop_id: int) -> DrmProperty:
        return self._props[prop_id]

    def find_property_id(self, obj: DrmPropObject, prop_name: str) -> int:
        # We may have duplicate names
        for prop_id in obj.prop_values:
            if self._props[prop_id].name == prop_name:
                return prop_id

        raise KeyError(f'{obj} has no property "{prop_name}"')

    def find_property_name(self, prop_id: int) -> str:
        return self._props[prop_id].name

    def set_defaults(self):
        try:
            self.set_master()
        except OSError:
            self.is_master = False

        cap = kms.uapi.drm_get_cap(kms.uapi.DRM_CAP_DUMB_BUFFER)
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_GET_CAP, cap, True)
        if not cap.value:
            raise NotImplementedError('Card does not support dumb buffers')

        try:
            self.set_client_cap(kms.uapi.DRM_CLIENT_CAP_UNIVERSAL_PLANES, 1)
        except OSError as e:
            raise NotImplementedError('Card does not support universal planes') from e

        try:
            self.set_client_cap(kms.uapi.DRM_CLIENT_CAP_ATOMIC, 1)
        except OSError as e:
            raise NotImplementedError('Card does not support atomic modesetting') from e

    def set_client_cap(self, capability: int, value: int):
        client_cap = kms.uapi.drm_set_client_cap(capability, value)
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_SET_CLIENT_CAP, client_cap, True)

    def set_master(self):
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_SET_MASTER, 0, False)
        self.is_master = True

    def drop_master(self):
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_DROP_MASTER, 0, False)
        self.is_master = False

    def get_version(self) -> Version:
        ver = kms.uapi.drm_version()
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_VERSION, ver, True)

        name = ctypes.create_string_buffer(ver.name_len)
        date = ctypes.create_string_buffer(ver.date_len)
        desc = ctypes.create_string_buffer(ver.desc_len)

        ver.name.raw = ctypes.cast(name, ctypes.POINTER(ctypes.c_char))
        ver.date.raw = ctypes.cast(date, ctypes.POINTER(ctypes.c_char))
        ver.desc.raw = ctypes.cast(desc, ctypes.POINTER(ctypes.c_char))

        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_VERSION, ver, True)

        return Version(
            ver.version_major,
            ver.version_minor,
            ver.version_patchlevel,
            name.value.decode(),
            date.value.decode(),
            desc.value.decode(),
        )

    def get_res(self):
        res = kms.uapi.drm_mode_card_res()
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETRESOURCES, res, True)

        fb_ids = (ctypes.c_uint32 * res.count_fbs)()
        res.fb_id_ptr = ctypes.addressof(fb_ids)

        crtc_ids = (ctypes.c_uint32 * res.count_crtcs)()
        res.crtc_id_ptr = ctypes.addressof(crtc_ids)

        connector_ids = (ctypes.c_uint32 * res.count_connectors)()
        res.connector_id_ptr = ctypes.addressof(connector_ids)

        encoder_ids = (ctypes.c_uint32 * res.count_encoders)()
        res.encoder_id_ptr = ctypes.addressof(encoder_ids)

        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETRESOURCES, res, True)

        self.crtcs = [Crtc(self, id, idx) for idx, id in enumerate(crtc_ids)]
        self.connectors = [Connector(self, id, idx) for idx, id in enumerate(connector_ids)]
        self.encoders = [Encoder(self, id, idx) for idx, id in enumerate(encoder_ids)]

    def get_plane_res(self):
        res = kms.uapi.drm_mode_get_plane_res()
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETPLANERESOURCES, res, True)

        plane_ids = (ctypes.c_uint32 * res.count_planes)()
        res.plane_id_ptr = ctypes.addressof(plane_ids)

        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETPLANERESOURCES, res, True)

        self.planes = [Plane(self, id, idx) for idx, id in enumerate(plane_ids)]

    def get_object(self, id: int) -> DrmObject:
        for ob in [*self.crtcs, *self.connectors, *self.encoders, *self.planes]:
            if ob.id == id:
                return ob

        raise KeyError(f'No object with id {id}')

    def get_connector(self, id: int) -> Connector:
        for ob in self.connectors:
            if ob.id == id:
                return ob

        raise KeyError(f'No connector with id {id}')

    def get_crtc(self, id: int) -> Crtc:
        for ob in self.crtcs:
            if ob.id == id:
                return ob

        raise KeyError(f'No CRTC with id {id}')

    def get_encoder(self, id: int) -> Encoder:
        for ob in self.encoders:
            if ob.id == id:
                return ob

        raise KeyError(f'No encoder with id {id}')

    def get_plane(self, id: int) -> Plane:
        for ob in self.planes:
            if ob.id == id:
                return ob

        raise KeyError(f'No plane with id {id}')

    def get_framebuffer(self, id):
        res = kms.uapi.drm_mode_fb_cmd2()
        res.fb_id = id
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETFB2, res, True)

        format = kms.PixelFormats.find_drm_fourcc(res.pixel_format)

        planes = []
        for i in range(len(format.planes)):
            p = Framebuffer.FramebufferPlane()
            p.handle = res.handles[i]
            p.pitch = res.pitches[i]
            p.offset = res.offsets[i]
            planes.append(p)

        return Framebuffer(self, res.fb_id, res.width, res.height, format, planes)

    def read_events(self) -> list[DrmEvent]:
        assert self.fio

        buf = self.event_buf

        l = self.fio.readinto(buf)
        if not l:
            return []

        assert l >= ctypes.sizeof(kms.uapi.drm_event)

        events = []

        i = 0
        while i < l:
            ev = kms.uapi.drm_event.from_buffer(buf, i)

            if ev.type in (kms.uapi.DRM_EVENT_VBLANK, kms.uapi.DRM_EVENT_FLIP_COMPLETE):
                vblank = kms.uapi.drm_event_vblank.from_buffer(buf, i)

                if ev.type == kms.uapi.DRM_EVENT_VBLANK:
                    ev_type = DrmEventType.VBLANK
                else:
                    ev_type = DrmEventType.FLIP_COMPLETE

                time = vblank.tv_sec + vblank.tv_usec / 1000000.0

                events.append(
                    DrmEvent(ev_type, vblank.sequence, time, vblank.user_data, vblank.crtc_id)
                )
            elif ev.type == kms.uapi.DRM_EVENT_CRTC_SEQUENCE:
                seq = kms.uapi.drm_event_crtc_sequence.from_buffer(buf, i)

                time = seq.time_ns / 1000000000.0

                events.append(
                    DrmEvent(DrmEventType.CRTC_SEQUENCE, seq.sequence, time, seq.user_data)
                )

            # Unknown event types are skipped

            i += ev.length

        return events

    def __repr__(self) -> str:
        return f'Card({self.dev_path})'

    def __str__(self) -> str:
        return self.dev_path
