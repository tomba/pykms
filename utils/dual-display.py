#!/usr/bin/env python3

import argparse
import sys
import kms
import kms.drawing

parser = argparse.ArgumentParser()
parser.add_argument('-c1', '--connector1', default='')
parser.add_argument('-c2', '--connector2', default='')
args = parser.parse_args()

PLANE_WIDTH = 300
PLANE_HEIGHT = 300

class Screen:
    def __init__(self, conn: kms.Connector, crtc: kms.Crtc) -> None:
        self.card = conn.card
        self.conn = conn
        self.crtc = crtc

        self.mode = conn.get_default_mode()
        self.modeb = self.mode.to_blob(self.card)

    def setup(self, req: kms.AtomicReq):
        req.add_connector(self.conn, self.crtc)
        req.add_crtc(self.crtc, self.modeb)


class Overlay:
    def __init__(self, plane: kms.Plane) -> None:
        self.plane = plane
        self.fb = kms.DumbFramebuffer(plane.card, PLANE_WIDTH, PLANE_HEIGHT, kms.PixelFormats.XRGB8888)
        nfb = kms.drawing.NumpyFramebuffer(self.fb)
        nfb.fill_rect(10, 10, 100, 100, kms.drawing.RGB(255, 255, 0, 0))

    def setup(self, req: kms.AtomicReq, screen: Screen):
        if self.plane.idx == 0:
            x = 0
        else:
            x = screen.mode.hdisplay - self.fb.width

        req.add_plane(self.plane, self.fb, screen.crtc, dst=(x, 0, self.fb.width, self.fb.height))

    def disable(self, req: kms.AtomicReq):
        req.add_plane(self.plane, fb=None, crtc=None)


def main():
    card = kms.Card()

    res = kms.ResourceManager(card)

    conn0 = res.reserve_connector(args.connector1)
    crtc0 = res.reserve_crtc(conn0)

    conn1 = res.reserve_connector(args.connector2)
    crtc1 = res.reserve_crtc(conn1)

    screen0 = Screen(conn0, crtc0)
    screen1 = Screen(conn1, crtc1)

    ovls = []
    for p in card.planes:
        ovls.append(Overlay(p))

    # TEST

    req = kms.AtomicReq(card)
    screen0.setup(req)
    screen1.setup(req)
    for o in ovls:
        o.disable(req)
    req.commit_sync(allow_modeset = True)
    print('Planes disabled'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[0].setup(req, screen0)
    ovls[1].setup(req, screen0)
    req.commit_sync(allow_modeset = True)
    print('Planes on Screen0'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[1].disable(req)
    req.commit_sync(allow_modeset = True)
    print('Plane1 disabled'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[1].setup(req, screen1)
    req.commit_sync(allow_modeset = True)
    print('Plane1 on Screen1'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[0].disable(req)
    req.commit_sync(allow_modeset = True)
    print('Plane0 disabled'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[0].setup(req, screen1)
    req.commit_sync(allow_modeset = True)
    print('Plane0 on Screen1'); sys.stdin.readline()





    req = kms.AtomicReq(card)
    ovls[1].disable(req)
    req.commit_sync(allow_modeset = True)
    print('Plane1 disabled'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[1].setup(req, screen0)
    req.commit_sync(allow_modeset = True)
    print('Plane1 on Screen0'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[0].disable(req)
    req.commit_sync(allow_modeset = True)
    print('Plane0 disabled'); sys.stdin.readline()

    req = kms.AtomicReq(card)
    ovls[0].setup(req, screen0)
    req.commit_sync(allow_modeset = True)
    print('Plane0 on Screen0'); sys.stdin.readline()



if __name__ == '__main__':
    main()
