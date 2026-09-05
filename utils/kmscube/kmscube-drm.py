#!/usr/bin/env python3

from __future__ import annotations

import os
import selectors
import sys
from typing import ClassVar

import kms

# It's hard to import from the current dir... So add the current directory to PYTHONPATH
sys.path.append(os.path.dirname(__file__))

os.environ['PYOPENGL_PLATFORM'] = 'egl'

from cube_egl import EglState, EglSurface
from cube_gl import GlScene
from gbm import GBM_BO_USE_RENDERING, GBM_BO_USE_SCANOUT, GBM_FORMAT_XRGB8888, GbmDevice


class GbmEglSurface:
    # Class-level cache of buffer objects to framebuffers
    _fb_cache: ClassVar[dict] = {}

    def __init__(self, card, gbm_dev: GbmDevice, egl_state: EglState, width: int, height: int):
        self.card = card
        self.egl = egl_state
        self.width = width
        self.height = height

        self.gbm_surface = gbm_dev.create_surface(
            width, height, GBM_FORMAT_XRGB8888, GBM_BO_USE_SCANOUT | GBM_BO_USE_RENDERING
        )

        self.egl_surface = EglSurface(self.egl, self.gbm_surface.handle)

        self.bo_prev = None
        self.bo_next = None

    def make_current(self):
        if not self.gbm_surface.has_free_buffers:
            raise RuntimeError('No free buffers')
        self.egl_surface.make_current()

    def swap_buffers(self):
        self.egl_surface.swap_buffers()

    def _create_framebuffer(self, bo):
        return kms.ExtFramebuffer(
            self.card, bo.width, bo.height, kms.PixelFormats.XRGB8888, [bo.handle], [bo.stride], [0]
        )

    def _get_fb_for_bo(self, bo):
        if bo not in self._fb_cache:
            self._fb_cache[bo] = self._create_framebuffer(bo)
        return self._fb_cache[bo]

    def lock_next(self):
        self.bo_prev = self.bo_next
        self.bo_next = self.gbm_surface.lock_front_buffer()
        if not self.bo_next:
            raise RuntimeError('Could not lock GBM buffer')

        return self._get_fb_for_bo(self.bo_next)

    def free_prev(self):
        if self.bo_prev:
            if self.bo_prev in self._fb_cache:
                del self._fb_cache[self.bo_prev]
            self.gbm_surface.release_buffer(self.bo_prev)
            self.bo_prev = None

    def __del__(self):
        if self.bo_next:
            if self.bo_next in self._fb_cache:
                del self._fb_cache[self.bo_next]
            self.gbm_surface.release_buffer(self.bo_next)


class OutputHandler:
    def __init__(
        self, card, gbm_dev, egl_state, connector, crtc, mode, modeb, plane, rotation_mult=1.0
    ):
        self.frame_num = 0
        self.connector = connector
        self.crtc = crtc
        self.plane = plane
        self.modeb = modeb
        self.rotation_mult = rotation_mult
        self.flip_pending = False
        self.card = crtc.card

        self.surface = GbmEglSurface(card, gbm_dev, egl_state, mode.hdisplay, mode.vdisplay)
        self.scene = GlScene()
        self.scene.set_viewport(self.surface.width, self.surface.height)

    def setup(self):
        # Initial buffer setup
        self.surface.make_current()
        self.surface.swap_buffers()
        fb = self.surface.lock_next()

        req = kms.AtomicReq(self.card)
        req.add_connector(self.connector, self.crtc)
        req.add_crtc(self.crtc, self.modeb)
        req.add_plane(self.plane, fb, self.crtc, dst=(0, 0, fb.width, fb.height))
        req.commit_sync(allow_modeset=True)

    def handle_page_flip(self, frame, cur_time):
        self.frame_num += 1

        self.surface.free_prev()
        self.flip_pending = False
        self.queue_next()

    def queue_next(self):
        self.surface.make_current()
        self.scene.draw(int(self.frame_num * self.rotation_mult))
        self.surface.swap_buffers()
        fb = self.surface.lock_next()

        req = kms.AtomicReq(self.crtc.card)
        req.add(self.plane, 'FB_ID', fb.id)
        req.commit()

        self.flip_pending = True


def main():
    card = kms.Card()
    res = kms.ResourceManager(card)
    conn = res.reserve_connector()
    crtc = res.reserve_crtc(conn)
    plane = res.reserve_plane(crtc)
    mode = conn.get_default_mode()
    modeb = mode.to_blob(card)

    gbm_dev = GbmDevice(card.fd)
    egl_state = EglState(gbm_dev.handle)

    rot_mult = 1.0

    out = OutputHandler(card, gbm_dev, egl_state, conn, crtc, mode, modeb, plane, rot_mult)

    out.setup()
    out.queue_next()

    sel = selectors.DefaultSelector()
    sel.register(card.fd, selectors.EVENT_READ)
    sel.register(sys.stdin, selectors.EVENT_READ)

    try:
        while True:
            events = sel.select()
            for key, mask in events:
                if key.fileobj == card.fd:
                    for ev in card.read_events():
                        if ev.type == kms.DrmEventType.FLIP_COMPLETE and out.flip_pending:
                            out.handle_page_flip(ev.seq, ev.time)
                            break

                elif key.fileobj == sys.stdin:
                    return

    except KeyboardInterrupt:
        pass
    finally:
        sel.close()


if __name__ == '__main__':
    main()
