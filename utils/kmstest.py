#!/usr/bin/python3

import argparse
import sys
import time

import numpy as np

from pixutils.dmaheap import DMAHeap
from kms.framebuffer import Framebuffer

import kms
import kms.uapi
import kms.drawing

def draw_pixel_xrgb8888(fb: Framebuffer, bufs, x, y, color: tuple):
    color = tuple(c >> 8 for c in color)
    bufs[0][y, x] = (color[0] << 16) | (color[1] << 8) | (color[2] << 0)

def draw_pixel_nv12(fb: Framebuffer, bufs, x, y, color: tuple):
    fmt = fb.format

    buf_y, buf_uv = bufs

    Y, Cb, Cr = (c >> 8 for c in color)

    macro_x = x
    macro_y = y
    buf_y[macro_y, macro_x] = Y

    macro_x = x // 2
    macro_y = y // fmt.planes[1].vsub

    shift_Cb = 0
    shift_Cr = 8

    buf_uv[macro_y, macro_x] = (Cb << shift_Cb) | (Cr << shift_Cr)

def draw_pixel_xv15(fb: Framebuffer, bufs, x, y, color: tuple):
    fmt = fb.format

    buf_y, buf_uv = bufs

    MASK10 = (1 << 10) - 1

    Y, Cb, Cr = (c >> 6 for c in color)

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
    v |= Y << shift_Y
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
    v |= (np.uint64(Cb) << np.uint64(shift_Cb)) | (np.uint64(Cr) << np.uint64(shift_Cr))
    buf_uv[UV_pos_unit[1], UV_pos_unit[0]] = v

def draw_pixel_grey(fb: Framebuffer, bufs, x, y, color: tuple):
    g = sum(c >> 8 for c in color) // 3
    bufs[0][y, x] = g

def draw_pixel_grey_y10_le32(fb: Framebuffer, bufs, x, y, color: tuple):
    g = sum(c >> 6 for c in color) // 3
    MASK10 = (1 << 10) - 1

    x_offset = x // 3
    x_mod = x % 3
    x_shift = x_mod * 10

    bufs[0][y, x_offset] &= ~(MASK10 << x_shift)
    bufs[0][y, x_offset] |= g << x_shift

def draw_pixel_x403(fb: Framebuffer, bufs, x, y, color: tuple):
    Y, Cb, Cr = (c >> 6 for c in color)

    MASK10 = (1 << 10) - 1

    x_offset = x // 3
    x_mod = x % 3
    x_shift = x_mod * 10

    bufs[0][y, x_offset] &= ~(MASK10 << x_shift)
    bufs[1][y, x_offset] &= ~(MASK10 << x_shift)
    bufs[2][y, x_offset] &= ~(MASK10 << x_shift)

    bufs[0][y, x_offset] |= Y << x_shift
    bufs[1][y, x_offset] |= Cb << x_shift
    bufs[2][y, x_offset] |= Cr << x_shift

def draw_pixel_xvuy2101010(fb: Framebuffer, bufs, x, y, color: tuple):
    Y, Cb, Cr = (c >> 6 for c in color)

    bufs[0][y, x] = (Y << 0) | (Cb << 10) | (Cr << 20)

def draw_pixel(fb: Framebuffer, bufs, x, y, color: tuple):
    fmt = fb.format

    if fmt == kms.PixelFormats.XRGB8888:
        draw_pixel_xrgb8888(fb, bufs, x, y, color)
    elif fmt in (kms.PixelFormats.XV15, kms.PixelFormats.XV20):
        draw_pixel_xv15(fb, bufs, x, y, color)
    elif fmt in (kms.PixelFormats.NV12, kms.PixelFormats.NV16):
        draw_pixel_nv12(fb, bufs, x, y, color)
    elif fmt == kms.PixelFormats.GREY8:
        draw_pixel_grey(fb, bufs, x, y, color)
    elif fmt == kms.PixelFormats.Y10_LE32:
        draw_pixel_grey_y10_le32(fb, bufs, x, y, color)
    elif fmt == kms.PixelFormats.X403:
        draw_pixel_x403(fb, bufs, x, y, color)
    elif fmt == kms.PixelFormats.XVUY2101010:
        draw_pixel_xvuy2101010(fb, bufs, x, y, color)

def prep_buffers(fb: Framebuffer):
    fmt = fb.format

    bufs: list[np.ndarray] = []

    # Create buffer views for pixel blocks
    for i,_ in enumerate(fmt.planes):
        bpb = fmt.planes[i].bytes_per_block

        assert bpb != 0

        buf = np.frombuffer(fb.map(i), dtype=np.dtype(f'<u{bpb}'))
        # Note: pitch already takes hsub into account
        buf = buf.reshape(fb.height // fmt.planes[i].vsub, fb.planes[i].pitch // bpb)
        bufs.append(buf)

    return bufs

def draw_test_pattern_new(fb: Framebuffer):
    bufs = prep_buffers(fb)

    if fb.format.color == kms.PixelColorEncoding.RGB:
        # (Red, Green, Blue)
        full = (0xffff, 0xffff, 0xffff)
        red = (0xffff, 0x0000, 0x0000)
        green = (0x0000, 0xffff, 0x0000)
        blue = (0x0000, 0x0000, 0xffff)
    elif fb.format.color == kms.PixelColorEncoding.YUV:
        # (Y, Cb, Cr)
        full = (0xffff, 0xffff, 0xffff)
        red = (0x4c00, 0x5400, 0xffff)
        green = (0x9500, 0x2b00, 0x1500)
        blue = (0x1d00, 0xffff, 0x6b00)
    else:
        assert False

    # Draw single pixel

    draw_pixel(fb, bufs,  400, 100, full)

    # Draw Diagonal

    for xy in range(0, fb.height):
        draw_pixel(fb, bufs, xy, xy, full)

    # Draw borders around the screen

    for y in [0, fb.height - 1]:
        for x in range(0, fb.width):
            draw_pixel(fb, bufs, x, y, full)

    for x in [0, fb.width - 1]:
        for y in range(0, fb.height):
            draw_pixel(fb, bufs, x, y, full)

    # Draw red, green, blue boxes

    box_size = fb.width // 16

    for y in range(box_size, box_size * 2):
        for x in range(box_size, box_size * 2):
            draw_pixel(fb, bufs, x, y, red)

    for y in range(box_size, box_size * 2):
        for x in range(box_size * 2, box_size * 3):
            draw_pixel(fb, bufs, x, y, green)

    for y in range(box_size, box_size * 2):
        for x in range(box_size * 3, box_size * 4):
            draw_pixel(fb, bufs, x, y, blue)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connector', default='')
    parser.add_argument('--dmabuf', nargs='?', const='reserved', metavar='HEAP', help='use dmabuf')
    parser.add_argument('-f', '--format', default='XRGB8888')
    args = parser.parse_args()

    fmt = kms.PixelFormats.find_by_name(args.format)

    card = kms.Card()

    res = kms.ResourceManager(card)
    conn = res.reserve_connector(args.connector)
    crtc = res.reserve_crtc(conn)
    plane = res.reserve_plane(crtc, format=fmt)
    mode = conn.get_default_mode()

    mode = next(m for m in conn.modes if m.hdisplay == 720)

    modeb = mode.to_blob(card)

    width = mode.hdisplay
    height = mode.vdisplay

    print(f'{width}x{height}-{fmt}')

    for idx,_ in enumerate(fmt.planes):
        print(f'Plane {idx}')

        ds = fmt.dumb_size(width, height, idx)
        print(f'\tdumb_size: {ds[0]}x{ds[1]}x{ds[2]/8} bytes={ds[0] * ds[1] * ds[2]/8}')

        print(f'\tstride={fmt.stride(width, idx)} planesize={fmt.planesize(width, height, idx)}')


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

    ts1 = time.perf_counter()
    fb.begin_cpu_access('w')

    draw_test_pattern_new(fb)

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
