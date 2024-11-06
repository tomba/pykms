#!/usr/bin/python3

import argparse
import sys
import time

import numpy as np

from kms.framebuffer import Framebuffer
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

def draw_pixel_xv15(fmt: kms.PixelFormat, buf_y, buf_uv, x, y, color: tuple):
    MASK10 = (1 << 10) - 1

    color_Y, color_Cb, color_Cr = color

    pos = (x, y)

    Y_pos = (pos[0] // fmt.planes[0].hsub, pos[1] // fmt.planes[0].vsub)
    UV_pos = (pos[0] // fmt.planes[1].hsub, pos[1] // fmt.planes[1].vsub)

    Y_offset = Y_pos[0] // 3
    Y_mod = Y_pos[0] % 3

    UV_offset = UV_pos[0] // 3
    UV_mod = UV_pos[0] % 3

    Y_pos_unit = (Y_offset, Y_pos[1])
    UV_pos_unit = (UV_offset, UV_pos[1])


    #print('pos:', pos, Y_pos, UV_pos)
    #print('Y offset ', Y_offset, 'mod', Y_mod)
    #print('UV offset ', UV_offset, 'mod', UV_mod)


    shift_Y = 10 * Y_mod

    v = buf_y[Y_pos_unit[1], Y_pos_unit[0]]
    v &= ~(MASK10 << shift_Y)
    v |= color_Y << shift_Y
    buf_y[Y_pos_unit[1], Y_pos_unit[0]] = v


    if UV_mod == 0:
        shift_Cb = 0
        shift_Cr = 10
    elif UV_mod == 1:
        shift_Cb = 20
        shift_Cr = 32
    elif UV_mod == 2:
        shift_Cb = 32 + 10
        shift_Cr = 32 + 20
    else:
        assert False

    v = buf_uv[UV_pos_unit[1], UV_pos_unit[0]]
    v &= ~((np.uint64(MASK10) << np.uint64(shift_Cb)) | (np.uint64(MASK10) << np.uint64(shift_Cr)))
    v |= (np.uint64(color_Cb) << np.uint64(shift_Cb)) | (np.uint64(color_Cr) << np.uint64(shift_Cr))
    buf_uv[UV_pos_unit[1], UV_pos_unit[0]] = v

def draw_test_pattern_xv15(fb: Framebuffer):
    fmt = fb.format

    buf_y = np.frombuffer(fb.map(0), dtype=np.dtype('<u4'))
    buf_y = buf_y.reshape(fb.height, fb.planes[0].pitch // 4)

    buf_uv = np.frombuffer(fb.map(1), dtype=np.dtype('<u8'))
    buf_uv = buf_uv.reshape(fb.height // 2, fb.planes[1].pitch // 8)

    # Draw single pixel

    draw_pixel_xv15(fmt, buf_y, buf_uv, 400, 100, (255 << 2, 255 << 2, 255 << 2))

    # Draw Diagonal

    for y in range(0, fb.height):
        draw_pixel_xv15(fmt, buf_y, buf_uv, y, y, (255 << 2, 255 << 2, 255 << 2))

    # Draw red, green, blue boxes

    red = (76 << 2, 84 << 2, 255 << 2)
    green = (149 << 2, 43 << 2, 21 << 2)
    blue = (29 << 2, 255 << 2, 107 << 2)

    for y in range(100, 150):
        for x in range(100, 150):
            draw_pixel_xv15(fmt, buf_y, buf_uv, x, y, red)

    for y in range(100, 150):
        for x in range(150, 200):
            draw_pixel_xv15(fmt, buf_y, buf_uv, x, y, green)

    for y in range(100, 150):
        for x in range(200, 250):
            draw_pixel_xv15(fmt, buf_y, buf_uv, x, y, blue)


def draw_pixel_nv12(buf_y, buf_uv, x, y, color):
    color_Y, color_Cb, color_Cr = color

    macro_x = x
    macro_y = y
    buf_y[macro_y, macro_x] = color_Y

    macro_x = x // 2
    macro_y = y // 2

    shift_Cb = 0
    shift_Cr = 8

    buf_uv[macro_y, macro_x] = (color_Cb << shift_Cb) | (color_Cr << shift_Cr)


def draw_test_pattern_nv12(fb):
    buf_y = np.frombuffer(fb.map(0), dtype=np.dtype('<u1')).reshape(fb.height, fb.planes[0].pitch)
    buf_uv = np.frombuffer(fb.map(1), dtype=np.dtype('<u2')).reshape(fb.height // 2, fb.planes[1].pitch // 2)

    # Draw single pixel

    draw_pixel_nv12(buf_y, buf_uv, 400, 100, (255, 255, 255))

    # Draw Diagonal

    for y in range(0, fb.height):
        draw_pixel_nv12(buf_y, buf_uv, y, y, (255, 255, 255))

    # Draw red, green, blue boxes

    red = (76, 84, 255)
    green = (149, 43, 21)
    blue = (29, 255, 107)

    for y in range(100, 150):
        for x in range(100, 150):
            draw_pixel_nv12(buf_y, buf_uv, x, y, red)

    for y in range(100, 150):
        for x in range(150, 200):
            draw_pixel_nv12(buf_y, buf_uv, x, y, green)

    for y in range(100, 150):
        for x in range(200, 250):
            draw_pixel_nv12(buf_y, buf_uv, x, y, blue)


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

    mode = next(m for m in conn.modes if m.hdisplay == 720)

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
    elif fmt == kms.PixelFormats.XV15:
        draw_test_pattern_xv15(fb)
    elif fmt == kms.PixelFormats.NV12:
        draw_test_pattern_nv12(fb)

    req = kms.AtomicReq(card)

    req.add_connector(conn, crtc)
    req.add_crtc(crtc, modeb)
    req.add_plane(plane, fb, crtc, dst=(0, 0, width, height))

    req.commit_sync(allow_modeset = True)

    input('press enter to exit\n')

if __name__ == '__main__':
    sys.exit(main())
