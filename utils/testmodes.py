#!/usr/bin/env python3

import argparse
import kms

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connector', default='')
parser.add_argument('-x', '--modeline', action='store_true', help='print modeline')
args = parser.parse_args()

card = kms.Card()

res = kms.ResourceManager(card)
conn = res.reserve_connector(args.connector)
crtc = res.reserve_crtc(conn)
plane = res.reserve_generic_plane(crtc)

kms.AtomicReq.disable_all(card)

for mode in conn.modes:
    if args.modeline:
        print(mode.to_str_modeline())
    else:
        print(mode.to_str())

    fb = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, kms.PixelFormats.XRGB8888)
    kms.draw_test_pattern(fb)

    kms.AtomicReq.set_mode(conn, crtc, fb, mode, plane)

    input('press enter to show next videomode\n')

print('done')
