#!/usr/bin/env python3

import argparse
import selectors
import sys

import pixpat
from pixutils.formats import PixelFormats

import kms
import kms.testpat

bar_width = 20
bar_speed = 8


def pixpat_sub_buffer(fb, x, width):
    fmt = fb.format
    sub_planes = []
    for i, p in enumerate(fb.planes):
        info = fmt.planes[i]
        if x % info.hsub != 0:
            raise ValueError(f'vbar x={x} not aligned to plane {i} hsub={info.hsub}')
        plane_x = x // info.hsub
        if plane_x % info.pixels_per_block != 0:
            raise ValueError(f'vbar x={x} not aligned to plane {i} pixels_per_block={info.pixels_per_block}')
        x_bytes = (plane_x // info.pixels_per_block) * info.bytes_per_block
        sub_planes.append(memoryview(fb.map(i))[x_bytes:])

    return pixpat.Buffer(
        planes=sub_planes,
        fmt=fmt.name,
        width=width,
        height=fb.height,
        strides=[p.pitch for p in fb.planes],
    )


def draw_vbar(fb, old_x, new_x, width):
    x_align = fb.format.pixel_align[0]
    if width % x_align != 0:
        raise ValueError(f'vbar width={width} not aligned to format x_align={x_align}')

    def snap(x):
        return x - (x % x_align)

    if old_x >= 0:
        x = snap(old_x)
        if x + width <= fb.width:
            sub = pixpat_sub_buffer(fb, x, width)
            pixpat.draw_pattern(sub, 'plain', params={'color': '000000'})

    if new_x >= 0:
        x = snap(new_x)
        if x + width <= fb.width:
            sub = pixpat_sub_buffer(fb, x, width)
            pixpat.draw_pattern(sub, 'vbar', params={'pos': 0, 'width': width})


class FlipHandler:
    def __init__(self, card, mode, fmt):
        super().__init__()
        self.bar_xpos = 0
        self.front_buf = 0
        self.fb1 = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, fmt)
        self.fb2 = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, fmt)
        self.flips = 0
        self.frames = 0
        self.time = 0

        for fb in (self.fb1, self.fb2):
            pixpat.draw_pattern(kms.testpat.pixpat_buffer(fb), 'plain',
                                params={'color': '000000'})

    def handle_page_flip(self, frame, time):
        self.flips += 1
        if self.time == 0:
            self.frames = frame
            self.time = time

        time_delta = time - self.time
        if time_delta >= 5:
            frame_delta = frame - self.frames
            print(f'Frame rate: {frame_delta / time_delta:f} ({self.flips}/{frame_delta} frames in {time_delta:f} s)')

            self.flips = 0
            self.frames = frame
            self.time = time

        if self.front_buf == 0:
            fb = self.fb2
        else:
            fb = self.fb1

        self.front_buf = self.front_buf ^ 1

        current_xpos = self.bar_xpos
        old_xpos = (current_xpos + (fb.width - bar_width - bar_speed)) % (fb.width - bar_width)
        new_xpos = (current_xpos + bar_speed) % (fb.width - bar_width)

        self.bar_xpos = new_xpos

        draw_vbar(fb, old_xpos, new_xpos, bar_width)

        ctx = kms.AtomicReq(card)
        ctx.add(crtc.primary_plane, 'FB_ID', fb.id)
        ctx.commit()


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connector', default='')
parser.add_argument('-f', '--format', dest='format', default='XRGB8888',
                    help='Pixel format (default: XRGB8888)')
args = parser.parse_args()

fmt = PixelFormats.find_by_name(args.format)

card = kms.Card()
res = kms.ResourceManager(card)
conn = res.reserve_connector(args.connector)
crtc = res.reserve_crtc(conn)
mode = conn.get_default_mode()

fliphandler = FlipHandler(card, mode, fmt)

kms.AtomicReq.set_mode(conn, crtc, fliphandler.fb1, mode)

fliphandler.handle_page_flip(0, 0)

def readdrm():
    for ev in card.read_events():
        if ev.type == kms.DrmEventType.FLIP_COMPLETE:
            fliphandler.handle_page_flip(ev.seq, ev.time)


def readkey():
    sys.stdin.readline()
    sys.exit(0)

sel = selectors.DefaultSelector()
sel.register(card.fd, selectors.EVENT_READ, readdrm)
sel.register(sys.stdin, selectors.EVENT_READ, readkey)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback()
