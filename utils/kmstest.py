#!/usr/bin/env python3

import argparse
import sys
import time

from pixutils.dmaheap import DMAHeap

import kms

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

    kms.testpat.draw_test_pattern(fb)

    ts1 = time.perf_counter()
    fb.begin_cpu_access('w')
    kms.testpat.draw_test_pattern(fb)
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
