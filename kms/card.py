from __future__ import annotations

import ctypes
import fcntl
import glob
import io
import os
import weakref

from kms.drmevent import DrmEvent, DrmEventType
from kms.drmproperty import DrmProperty
from kms.drmpropobject import DrmPropObject
from kms.connector import Connector
from kms.encoder import Encoder
from kms.crtc import Crtc
from kms.plane import Plane
from kms.framebuffer import Framebuffer

import kms.uapi

__all__ = [
    'Card',
]

class Card:
    def __init__(self, dev_path: str | None = None) -> None:
        if not dev_path:
            dev_path = Card.__open_first_kms_device()

        self.dev_path = dev_path

        self.fio = io.FileIO(dev_path,
                             opener=lambda name,_: os.open(name, os.O_RDWR | os.O_NONBLOCK))

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

    def find_property(self, prop_id: int):
        return self._props[prop_id]

    def find_property_id(self, obj: DrmPropObject, prop_name: str):
        # We may have duplicate names
        return next(id for id in obj.prop_values if self._props[id].name == prop_name)

    def find_property_name(self, prop_id):
        return self._props[prop_id].name

    def set_defaults(self):
        try:
            fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_SET_MASTER, 0, False)
            self.is_master = True
        except OSError:
            self.is_master = False

        cap = kms.uapi.drm_get_cap(kms.uapi.DRM_CAP_DUMB_BUFFER)
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_GET_CAP, cap, True)
        if not cap.value:
            raise NotImplementedError('Card does not support dumb buffers')

        client_cap = kms.uapi.drm_set_client_cap(kms.uapi.DRM_CLIENT_CAP_UNIVERSAL_PLANES, 1)
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_SET_CLIENT_CAP, client_cap, True)
        if not cap.value:
            raise NotImplementedError('Card does not support universal planes')

        client_cap = kms.uapi.drm_set_client_cap(kms.uapi.DRM_CLIENT_CAP_ATOMIC, 1)
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_SET_CLIENT_CAP, client_cap, True)
        if not cap.value:
            raise NotImplementedError('Card does not support atomic modesetting')

    def drop_master(self):
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_DROP_MASTER, 0, False)

    def get_version(self):
        ver = kms.uapi.drm_version()
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_VERSION, ver, True)

        ver.name = kms.uapi.String(b' ' * ver.name_len)
        ver.date = kms.uapi.String(b' ' * ver.date_len)
        ver.desc = kms.uapi.String(b' ' * ver.desc_len)

        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_VERSION, ver, True)

        return ver

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

        self.crtcs = [Crtc(self, id, idx) for idx,id in enumerate(crtc_ids)]
        self.connectors = [Connector(self, id, idx) for idx,id in enumerate(connector_ids)]
        self.encoders = [Encoder(self, id, idx) for idx,id in enumerate(encoder_ids)]

    def get_plane_res(self):
        res = kms.uapi.drm_mode_get_plane_res()
        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETPLANERESOURCES, res, True)

        plane_ids = (ctypes.c_uint32 * res.count_planes)()
        res.plane_id_ptr = ctypes.addressof(plane_ids)

        fcntl.ioctl(self.fd, kms.uapi.DRM_IOCTL_MODE_GETPLANERESOURCES, res, True)

        self.planes = [Plane(self, id, idx) for idx,id in enumerate(plane_ids)]

    def get_object(self, id):
        return next(ob for ob in [*self.crtcs, *self.connectors, *self.encoders, *self.planes] if ob.id == id)

    def get_connector(self, id):
        return next(ob for ob in self.connectors if ob.id == id)

    def get_crtc(self, id):
        return next(ob for ob in self.crtcs if ob.id == id)

    def get_encoder(self, id):
        return next(ob for ob in self.encoders if ob.id == id)

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
        assert(self.fio)

        buf = self.event_buf

        l = self.fio.readinto(buf)
        if not l:
            return []

        assert (l >= ctypes.sizeof(kms.uapi.drm_event))

        events = []

        i = 0
        while i < l:
            ev = kms.uapi.drm_event.from_buffer(buf, i)

            #print(f'event type{ev.type}, len {ev.length}')

            if ev.type == kms.uapi.DRM_EVENT_VBLANK:
                raise NotImplementedError()
            elif ev.type == kms.uapi.DRM_EVENT_FLIP_COMPLETE:
                vblank = kms.uapi.drm_event_vblank.from_buffer(buf, i)
                #print(vblank.sequence, vblank.tv_sec, vblank.tv_usec, vblank.crtc_id, vblank.user_data)

                time = vblank.tv_sec + vblank.tv_usec / 1000000.0

                events.append(DrmEvent(DrmEventType.FLIP_COMPLETE, vblank.sequence, time, vblank.user_data))

            elif ev.type == kms.uapi.DRM_EVENT_CRTC_SEQUENCE:
                raise NotImplementedError()
            else:
                raise NotImplementedError()

            i += ev.length

        return events

    def __repr__(self) -> str:
        return f'Card({self.dev_path})'

    def __str__(self) -> str:
        return self.dev_path
