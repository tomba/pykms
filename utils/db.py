#!/usr/bin/env python3

import sys
import selectors
import kms
import kms.drawing

bar_width = 20
bar_speed = 8

class FlipHandler:
    def __init__(self):
        super().__init__()
        self.bar_xpos = 0
        self.front_buf = 0
        self.fb1 = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, kms.PixelFormats.XRGB8888)
        self.fb2 = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, kms.PixelFormats.XRGB8888)
        self.flips = 0
        self.frames = 0
        self.time = 0

        self.nfb1 = kms.drawing.NumpyFramebuffer(self.fb1, prepopulate=True)
        self.nfb2 = kms.drawing.NumpyFramebuffer(self.fb2, prepopulate=True)

    def handle_page_flip(self, frame, time):
        self.flips += 1
        if self.time == 0:
            self.frames = frame
            self.time = time

        time_delta = time - self.time
        if time_delta >= 5:
            frame_delta = frame - self.frames
            print('Frame rate: %f (%u/%u frames in %f s)' %
                  (frame_delta / time_delta, self.flips, frame_delta, time_delta))

            self.flips = 0
            self.frames = frame
            self.time = time

        if self.front_buf == 0:
            fb = self.fb2
            nfb = self.nfb2
        else:
            fb = self.fb1
            nfb = self.nfb1

        self.front_buf = self.front_buf ^ 1

        current_xpos = self.bar_xpos
        old_xpos = (current_xpos + (fb.width - bar_width - bar_speed)) % (fb.width - bar_width)
        new_xpos = (current_xpos + bar_speed) % (fb.width - bar_width)

        self.bar_xpos = new_xpos

        nfb.draw_color_bar(old_xpos, new_xpos, bar_width)

        ctx = kms.AtomicReq(card)
        ctx.add(crtc.primary_plane, 'FB_ID', fb.id)
        ctx.commit()

if len(sys.argv) > 1:
    conn_name = sys.argv[1]
else:
    conn_name = ''

card = kms.Card()
res = kms.ResourceManager(card)
conn = res.reserve_connector(conn_name)
crtc = res.reserve_crtc(conn)
mode = conn.get_default_mode()

fliphandler = FlipHandler()

kms.AtomicReq.set_mode(conn, crtc, fliphandler.fb1, mode)

fliphandler.handle_page_flip(0, 0)

def readdrm():
    for ev in card.read_events():
        if ev.type == kms.DrmEventType.FLIP_COMPLETE:
            fliphandler.handle_page_flip(ev.seq, ev.time)


def readkey():
    #print("KEY EVENT")
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
