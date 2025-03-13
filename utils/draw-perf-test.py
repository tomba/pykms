#!/usr/bin/env python3

from __future__ import annotations

import argparse
import selectors
import sys
import time
import numpy as np
import kms

class State:
    def __init__(self, card, conn, crtc, plane, mode) -> None:
        self.card = card
        self.conn = conn
        self.crtc = crtc
        self.plane = plane
        self.mode = mode
        self.modeb = mode.to_blob(card)
        self.fbs = []
        self.custom_state = {}

        self.current_fb: None | int = None
        self.next_fb = 0
        self.bar_y = 0
        self.last_ts = time.perf_counter()
        self.last_framenum = 0
        self.framenum = 0
        self.bar_step = 4

        self.test_mode = 0

# Test with direct mmap access

def init_fbs_0(state: State):
    mmaps = []

    for fb in state.fbs:
        fb_mmaps = fb.mmap()
        buf = fb_mmaps[0]
        buf[:] = bytearray(fb.planes[0].size)

        mmaps.append(fb_mmaps)

    state.custom_state = {
        'mmaps': mmaps,
        'line_0': bytes([0] * (state.mode.hdisplay * 4)),
        'line_1': bytes([0xff] * (state.mode.hdisplay * 4)),
    }

def draw_fb_0(state: State, fb_idx: int, old_y):
    fb = state.fbs[fb_idx]

    m = state.custom_state['mmaps'][fb_idx][0]
    pitch = fb.planes[0].pitch

    m[old_y * pitch:old_y * pitch + fb.width * 4] = state.custom_state['line_0']
    m[state.bar_y * pitch:state.bar_y * pitch + fb.width * 4] = state.custom_state['line_1']


# Test with mmap + numpy

def init_fbs_1(state: State):
    numpybufs = []

    for fb in state.fbs:
        fb_mmaps = fb.mmap()
        buf = fb_mmaps[0]

        b = np.frombuffer(buf, dtype=np.uint32).reshape(fb.height, fb.width)

        b[:] = 0x000000

        numpybufs.append(b)

    state.custom_state = {
        'numpybufs': numpybufs,
    }

def draw_fb_1(state: State, fb_idx: int, old_y):
    b = state.custom_state['numpybufs'][fb_idx]
    b[old_y, :] = 0
    b[state.bar_y, :] = 0xffffff


def init_fbs(state: State):
    if state.test_mode == 0:
        init_fbs_0(state)
    elif state.test_mode == 1:
        init_fbs_1(state)
    else:
        raise RuntimeError()

def draw_fb(state: State, fb_idx: int, old_y):
    if state.test_mode == 0:
        draw_fb_0(state, fb_idx, old_y)
    elif state.test_mode == 1:
        draw_fb_1(state, fb_idx, old_y)
    else:
        raise RuntimeError()

def handle_fps(state: State):
    ts = time.perf_counter()
    ts_diff = ts - state.last_ts

    if ts_diff > 2:
        num_frames = state.framenum - state.last_framenum

        fps = num_frames / ts_diff

        state.last_ts = ts
        state.last_framenum = state.framenum

        print(f'fps {fps:.2f}')

def handle_pageflip(state: State):
    state.framenum += 1

    handle_fps(state)

    #print("FLIP, cur", state.current_fb, "next", state.next_fb)

    old_fb = state.current_fb
    state.current_fb = state.next_fb
    state.next_fb = (state.current_fb + 1) % len(state.fbs)

    req = kms.AtomicReq(state.card)
    req.add_plane(state.plane, state.fbs[state.next_fb], state.crtc, dst=(0, 0, state.mode.hdisplay, state.mode.vdisplay))
    req.commit(allow_modeset = False)

    old_y = state.bar_y - len(state.fbs) * state.bar_step
    if old_y < 0:
        old_y = state.mode.vdisplay + old_y

    if old_fb is not None:
        ts1 = time.perf_counter()

        draw_fb(state, old_fb, old_y)

        ts2 = time.perf_counter()

        print(f'         {(ts2 - ts1) * 1000000:.4f} us')

        state.bar_y += state.bar_step
        if state.bar_y >= state.mode.vdisplay:
            state.bar_y = 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connector', default='')
    parser.add_argument('-m', '--mode', type=int, default=0)
    args = parser.parse_args()

    card = kms.Card()

    res = kms.ResourceManager(card)
    conn = res.reserve_connector(args.connector)
    crtc = res.reserve_crtc(conn)
    plane = res.reserve_plane(crtc, kms.PixelFormats.XRGB8888)
    mode = conn.get_default_mode()

    state = State(card, conn, crtc, plane, mode)
    state.test_mode = args.mode

    for _ in range(3):
        fb = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, kms.PixelFormats.XRGB8888)
        state.fbs.append(fb)

    init_fbs(state)

    req = kms.AtomicReq(card)

    req.add_connector(conn, crtc)
    req.add_crtc(crtc, state.modeb)
    req.add_plane(plane, state.fbs[2], crtc, dst=(0, 0, mode.hdisplay, mode.vdisplay))

    req.commit(allow_modeset = True)

    def readdrm(state: State):
        for ev in card.read_events():
            if ev.type == kms.DrmEventType.FLIP_COMPLETE:
                handle_pageflip(state)

    def readkey(_: State):
        print('Done')
        sys.stdin.readline()
        sys.exit(0)

    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ, readkey)
    sel.register(card.fd, selectors.EVENT_READ, readdrm)

    while True:
        events = sel.select()
        for key, _ in events:
            callback = key.data
            callback(state)

if __name__ == '__main__':
    sys.exit(main())
