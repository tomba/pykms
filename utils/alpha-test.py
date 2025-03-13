#!/usr/bin/env python3

import argparse
import time
import kms
from kms import drawing

parser = argparse.ArgumentParser(description='Simple alpha blending test.')
parser.add_argument('--resetcrtc', action='store_true',
                    help='Reset legacy CRTC color properties')
parser.add_argument('--connector', '-c', dest='connector', default='',
                    required=False, help='connector to output')
parser.add_argument('--mode', '-m', dest='modename',
                    required=False, help='Video mode name to use')
args = parser.parse_args()

max_planes = 4

card = kms.Card()
res = kms.ResourceManager(card)
conn = res.reserve_connector(args.connector)
crtc = res.reserve_crtc(conn)
if args.modename is None:
    mode = conn.get_default_mode()
else:
    mode = conn.get_mode(args.modename)

planes = []

for i in range(max_planes):
    p = res.reserve_generic_plane(crtc)
    if p is None:
        break
    planes.append(p)

print('Got {} planes. Test supports up to 4 planes.'.format(len(planes)))

w = mode.hdisplay
h = mode.vdisplay

fbs=[]

for i in range(max_planes):
    fb = kms.DumbFramebuffer(card, w, h, kms.PixelFormats.ARGB8888)
    fbs.append(drawing.NumpyFramebuffer(fb))

fbs[0].fill_rect(50, 50, 200, 200, drawing.RGB(128, 255, 0, 0))
fbs[1].fill_rect(150, 50, 200, 200, drawing.RGB(128, 0, 255, 0))
fbs[2].fill_rect(50, 150, 200, 200, drawing.RGB(128, 0, 0, 255))
fbs[3].fill_rect(150, 150, 200, 200, drawing.RGB(128, 128, 128, 128))

if args.resetcrtc:
    crtc.set_props({
        'trans-key-mode': 0,
        'trans-key': 0,
        'background': 0,
        'alpha_blender': 1,
    })

for i, plane in enumerate(planes):
    fb = fbs[i]

    print('set crtc {}, plane {}, z {}, fb {}'.format(crtc.id, plane.id, i, fb.id))

    plane.set_props({
        'FB_ID': fb.id,
        'CRTC_ID': crtc.id,
        'SRC_W': fb.width << 16,
        'SRC_H': fb.height << 16,
        'CRTC_W': fb.width,
        'CRTC_H': fb.height,
        'zpos': i,
    })

    time.sleep(1)

input('press enter to exit\n')
