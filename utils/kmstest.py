#!/usr/bin/env python3

import argparse
import sys
import time

import numpy as np

from pixutils.dmaheap import DMAHeap

import kms
import kms.uapi
import kms.drawing

def draw_test_pattern(fb):
    nfb = kms.drawing.NumpyFramebuffer(fb)

    nfb.fill_rect(2, 2, 200, 200, 0xff0000)
    nfb.fill_rect(202, 202, 200, 200, 0x00ff00)
    nfb.fill_rect(402, 402, 200, 200, 0x0000ff)
    nfb.fill_rect(202, 2, 200, 200, 0xffff00)
    nfb.fill_rect(402, 202, 200, 200, 0x00ffff)
    nfb.fill_rect(402, 2, 200, 200, 0xffffff)

    gradient = np.arange(256 - 1, -1, -1, dtype=np.uint32)

    nfb.draw_gradient(800, 2, 200, gradient << 16)
    nfb.draw_gradient(800, 202, 200, gradient << 8)
    nfb.draw_gradient(800, 402, 200, gradient << 0)

    nfb.b[0::fb.height-1, :] = 0xffffff
    nfb.b[:, 0::fb.width-1] = 0xffffff

    # Diagonals
    d1 = nfb.b.ravel()
    d1[0::fb.width+1] = 0xffffff
    d1[fb.width-1::fb.width-1] = 0xffffff

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connector', default='')
    parser.add_argument('--dmabuf', nargs='?', const='reserved', metavar='HEAP', help='use dmabuf')
    parser.add_argument('-f', '--format', default='XRGB8888')
    args = parser.parse_args()

    card = kms.Card()

    res = kms.ResourceManager(card)
    conn = res.reserve_connector(args.connector)
    crtc = res.reserve_crtc(conn)
    plane = res.reserve_generic_plane(crtc)
    mode = conn.get_default_mode()

    print(mode)

    modeb = mode.to_blob(card)

    fmt = kms.PixelFormats.find_by_name(args.format)

    width = mode.hdisplay
    height = mode.vdisplay

    if args.dmabuf:
        heap = DMAHeap(args.dmabuf)
        heap_buf = heap.alloc(fmt.framesize(width, height))

        fb = kms.DmabufFramebuffer(card, width, height,
                                   fmt,
                                   fds=[ heap_buf.fd ],
                                   pitches=[ fmt.stride(width) ],
                                   offsets=[ 0 ])
    else:
        fb = kms.DumbFramebuffer(card, width, height, fmt)

    if fmt == kms.PixelFormats.XRGB8888:
        ts1 = time.perf_counter()
        fb.begin_cpu_access('w')
        draw_test_pattern(fb)
        fb.end_cpu_access()
        ts2 = time.perf_counter()
        print(f'Drawing took {(ts2 - ts1) * 1000:.4f} ms')

    req = kms.AtomicReq(card)

    req.add_connector(conn, crtc)
    req.add_crtc(crtc, modeb)
    req.add_plane(plane, fb, crtc, dst=(0, 0, width, height))

    req.commit_sync(allow_modeset = True)

    input('press enter to exit\n')

if __name__ == '__main__':
    sys.exit(main())
