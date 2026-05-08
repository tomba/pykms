#!/usr/bin/env python3

import argparse
import sys

import kms
import kms.testpat

def test_fmt(conn, crtc, plane, mode, modeb, fmt):
    card = conn.card

    try:
        fb = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, fmt)
    except Exception as e:
        print(f'Skipping format {fmt}: unable to create dumb fb: {e}')
        return

    try:
        kms.testpat.draw_test_pattern(fb)
    except Exception as e:
        print(f'Skipping format {fmt}: unable to draw test pattern: {e}')
        return

    req = kms.AtomicReq(card)

    req.add_connector(conn, crtc)
    req.add_crtc(crtc, modeb)
    req.add_plane(plane, fb, crtc, dst=(0, 0, mode.hdisplay, mode.vdisplay))

    req.commit_sync(allow_modeset = True)

    input('press enter to continue\n')

def tests(conn, crtc, plane, mode, formats):
    print(f'Test formats: {list(fmt.name for fmt in formats)}')

    card = conn.card

    modeb = mode.to_blob(card)

    for fmt in formats:
        print(f'Test {fmt}')

        test_fmt(conn, crtc, plane, mode, modeb, fmt)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connector', default='')
    parser.add_argument('-p', '--plane', type=int, default=0)
    parser.add_argument('-f', '--format')
    args = parser.parse_args()

    card = kms.Card()

    res = kms.ResourceManager(card)
    conn = res.reserve_connector(args.connector)
    crtc = res.reserve_crtc(conn)
    mode = conn.get_default_mode()

    planes = crtc.get_possible_planes()
    if args.plane >= len(planes):
        raise ValueError('Plane index too large')
    plane = planes[args.plane]

    if args.format:
        format = kms.PixelFormats.find_by_name(args.format)
        formats = [format]
    else:
        formats = plane.format_types

    tests(conn, crtc, plane, mode, formats)

    print('all done')

if __name__ == '__main__':
    sys.exit(main())
