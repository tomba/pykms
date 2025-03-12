from __future__ import annotations

import ctypes
import fcntl
import mmap
import os
import weakref

from typing import TYPE_CHECKING

import pixutils.ioctl

import kms
import kms.uapi

if TYPE_CHECKING:
    from kms import Card

__all__ = [ 'Framebuffer', 'DumbFramebuffer', 'DmabufFramebuffer', 'ExtFramebuffer' ]

class Framebuffer(kms.DrmObject):
    class FramebufferPlane:
        def __init__(self) -> None:
            self.handle = 0
            self.pitch = 0
            self.size = 0
            self.prime_fd = -1
            self.offset = 0
            self.map: mmap.mmap | None = None

    def __init__(self, card: Card, id: int, width: int, height: int, format: kms.PixelFormat, planes: list[FramebufferPlane]) -> None:
        super().__init__(card, id, kms.uapi.DRM_MODE_OBJECT_FB, -1)

        self.width = width
        self.height = height
        self.format = format
        self.planes = planes

    def size(self, plane_idx):
        return self.planes[plane_idx].size

    def map(self, plane_idx: int) -> mmap.mmap:
        raise NotImplementedError()

    def mmap(self) -> list[mmap.mmap]:
        return [self.map(pidx) for pidx in range(len(self.planes))]

    def clear(self):
        for idx in range(len(self.planes)):
            # Can't we just create a ubyte pointer type and use it, instead of
            # creating a ubyte[planesize] type for each plane?
            ptrtype = ctypes.c_ubyte * self.size(idx)
            ptr = ptrtype.from_buffer(self.map(idx))
            ctypes.memset(ptr, 0, self.size(idx))

    def begin_cpu_access(self, access: str):
        raise NotImplementedError()

    def end_cpu_access(self):
        raise NotImplementedError()


class DumbFramebuffer(Framebuffer):
    def __init__(self, card: Card, width: int, height: int, format: kms.PixelFormat) -> None:
        planes = []

        for idx, _ in enumerate(format.planes):
            creq = kms.uapi.drm_mode_create_dumb()

            creq.width, creq.height, creq.bpp = format.dumb_size(width, height, idx)

            fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_CREATE_DUMB, creq, True)

            plane = Framebuffer.FramebufferPlane()
            plane.handle = creq.handle
            plane.pitch = creq.pitch
            plane.size = creq.height * creq.pitch

            planes.append(plane)

        fb2 = kms.uapi.struct_drm_mode_fb_cmd2()
        fb2.width = width
        fb2.height = height
        fb2.pixel_format = format.drm_fourcc
        fb2.handles = (ctypes.c_uint * 4)(*[p.handle for p in planes])
        fb2.pitches = (ctypes.c_uint * 4)(*[p.pitch for p in planes])
        fb2.offsets = (ctypes.c_uint * 4)(*[p.offset for p in planes])

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_ADDFB2, fb2, True)

        super().__init__(card, fb2.fb_id, width, height, format, planes)

        weakref.finalize(self, DumbFramebuffer.cleanup, self.card, self.id, planes)

    @staticmethod
    def cleanup(card: Card, fb_id: int, planes: list[Framebuffer.FramebufferPlane]):
        for p in planes:
            if p.prime_fd != -1:
                os.close(p.prime_fd)
                p.prime_fd = -1

            if p.map:
                try:
                    # This will fail if the user is still using the mmap,
                    # e.g. a numpy buffer.
                    p.map.close()
                except BufferError:
                    print('Warning: mmapped buffer still in use')
                finally:
                    p.map = None

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_RMFB, ctypes.c_uint32(fb_id), False)

        for p in planes:
            dumb = kms.uapi.drm_mode_destroy_dumb()
            dumb.handle = p.handle
            fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_DESTROY_DUMB, dumb, True)

    def __repr__(self) -> str:
        return f'DumbFramebuffer({self.id})'

    def map(self, plane_idx):
        p = self.planes[plane_idx]

        if p.offset == 0:
            map_dumb = kms.uapi.struct_drm_mode_map_dumb()
            map_dumb.handle = p.handle
            fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_MAP_DUMB, map_dumb, True)
            p.offset = map_dumb.offset

        if not p.map:
            p.map = mmap.mmap(self.card.fd, p.size,
                              mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE,
                              offset=p.offset)

        return p.map

    def fd(self, plane_idx):
        p = self.planes[plane_idx]

        if p.prime_fd != -1:
            return p.prime_fd

        args = kms.uapi.drm_prime_handle()
        args.handle = self.planes[plane_idx].handle
        args.fd = -1
        args.flags = os.O_CLOEXEC | os.O_RDWR
        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_PRIME_HANDLE_TO_FD, args, True)

        p.prime_fd = args.fd

        return p.prime_fd

    def begin_cpu_access(self, access: str):
        pass

    def end_cpu_access(self):
        pass


class DmabufFramebuffer(Framebuffer):
    class struct_dma_buf_sync(ctypes.Structure):
        __slots__ = ['flags']
        _fields_ = [('flags', ctypes.c_uint64)]

    DMA_BUF_BASE = 'b'
    DMA_BUF_IOCTL_SYNC = pixutils.ioctl.IOW(DMA_BUF_BASE, 0, struct_dma_buf_sync)

    DMA_BUF_SYNC_READ = 1 << 0
    DMA_BUF_SYNC_WRITE = 2 << 0
    DMA_BUF_SYNC_RW = DMA_BUF_SYNC_READ | DMA_BUF_SYNC_WRITE
    DMA_BUF_SYNC_START = 0 << 2
    DMA_BUF_SYNC_END = 1 << 2

    def __init__(self, card: Card, width: int, height: int, format: kms.PixelFormat,
                 fds: list[int], pitches: list[int], offsets: list[int]) -> None:
        planes = []

        self._sync_flags = 0

        fds = [os.dup(fd) for fd in fds]

        for idx in range(len(format.planes)):
            args = kms.uapi.drm_prime_handle(fd=fds[idx])
            fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_PRIME_FD_TO_HANDLE, args, True)

            plane = Framebuffer.FramebufferPlane()
            plane.handle = args.handle
            plane.pitch = pitches[idx]
            plane.size = format.planesize(plane.pitch, height, idx)
            plane.prime_fd = fds[idx]
            plane.offset = offsets[idx]
            planes.append(plane)

        fb2 = kms.uapi.struct_drm_mode_fb_cmd2()
        fb2.width = width
        fb2.height = height
        fb2.pixel_format = format.drm_fourcc
        fb2.handles = (ctypes.c_uint * 4)(*[p.handle for p in planes])
        fb2.pitches = (ctypes.c_uint * 4)(*[p.pitch for p in planes])
        fb2.offsets = (ctypes.c_uint * 4)(*[p.offset for p in planes])

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_ADDFB2, fb2, True)

        super().__init__(card, fb2.fb_id, width, height, format, planes)

        weakref.finalize(self, DmabufFramebuffer.cleanup, self.card, self.id, self.planes)

    @staticmethod
    def cleanup(card: Card, fb_id: int, planes: list[Framebuffer.FramebufferPlane]):
        for p in planes:
            if p.prime_fd != -1:
                os.close(p.prime_fd)
                p.prime_fd = -1

            if p.map:
                try:
                    # This will fail if the user is still using the mmap,
                    # e.g. a numpy buffer.
                    p.map.close()
                except BufferError:
                    print('Warning: mmapped buffer still in use')
                finally:
                    p.map = None

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_RMFB, ctypes.c_uint32(fb_id), False)

    def __repr__(self) -> str:
        return f'DmabufFramebuffer({self.id})'

    def map(self, plane_idx):
        p = self.planes[plane_idx]

        if not p.map:
            p.map = mmap.mmap(p.prime_fd, p.size,
                              mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)

        return p.map

    def fd(self, plane_idx):
        p = self.planes[plane_idx]

        return p.prime_fd

    def begin_cpu_access(self, access: str):
        if self._sync_flags != 0:
            raise RuntimeError('begin_cpu sync already started')

        if access == 'r':
            self._sync_flags = DmabufFramebuffer.DMA_BUF_SYNC_READ
        elif access == 'w':
            self._sync_flags = DmabufFramebuffer.DMA_BUF_SYNC_WRITE
        elif access == 'rw':
            self._sync_flags = DmabufFramebuffer.DMA_BUF_SYNC_RW
        else:
            raise RuntimeError('Bad access type "{access}"')

        dbs = DmabufFramebuffer.struct_dma_buf_sync()
        # pylint: disable=attribute-defined-outside-init
        dbs.flags = DmabufFramebuffer.DMA_BUF_SYNC_START | self._sync_flags

        for p in self.planes:
            fcntl.ioctl(p.prime_fd, DmabufFramebuffer.DMA_BUF_IOCTL_SYNC, dbs, False)

    def end_cpu_access(self):
        if self._sync_flags == 0:
            raise RuntimeError('begin_cpu sync not started')

        dbs = DmabufFramebuffer.struct_dma_buf_sync()
        # pylint: disable=attribute-defined-outside-init
        dbs.flags = DmabufFramebuffer.DMA_BUF_SYNC_END | self._sync_flags

        for p in self.planes:
            fcntl.ioctl(p.prime_fd, DmabufFramebuffer.DMA_BUF_IOCTL_SYNC, dbs, False)

        self._sync_flags = 0

class ExtFramebuffer(Framebuffer):
    def __init__(self, card: Card, width: int, height: int, format: kms.PixelFormat,
                 handles: list[int], pitches: list[int], offsets: list[int]):
        planes = []

        for idx in range(len(format.planes)):
            plane = Framebuffer.FramebufferPlane()
            plane.handle = handles[idx]
            plane.pitch = pitches[idx]
            plane.size = format.planesize(plane.pitch, height, idx)
            plane.offset = offsets[idx]
            planes.append(plane)

        fb2 = kms.uapi.struct_drm_mode_fb_cmd2()
        fb2.width = width
        fb2.height = height
        fb2.pixel_format = format.drm_fourcc
        fb2.handles = (ctypes.c_uint * 4)(*[p.handle for p in planes])
        fb2.pitches = (ctypes.c_uint * 4)(*[p.pitch for p in planes])
        fb2.offsets = (ctypes.c_uint * 4)(*[p.offset for p in planes])

        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_ADDFB2, fb2, True)

        super().__init__(card, fb2.fb_id, width, height, format, planes)

        weakref.finalize(self, ExtFramebuffer.cleanup, self.card, self.id, self.planes)

    @staticmethod
    def cleanup(card: Card, fb_id: int, planes: list[Framebuffer.FramebufferPlane]):
        fcntl.ioctl(card.fd, kms.uapi.DRM_IOCTL_MODE_RMFB, ctypes.c_uint32(fb_id), False)
