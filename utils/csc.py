#!/usr/bin/env python3

import argparse
import sys

import kms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connector', default='')
    parser.add_argument('-f', '--format', default='NV12')
    parser.add_argument('--pattern', default='')
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

    enc_prop_id = card.find_property_id(plane, 'COLOR_ENCODING')
    range_prop_id = card.find_property_id(plane, 'COLOR_RANGE')

    # Keep a ref to the old framebuffer to prevent it from being freed
    old_fb = None

    for rec_standard in kms.testpat.RecStandard:
        for full_range in kms.testpat.ColorRange:
            print(f'Format: {fmt} Encoding: {rec_standard}, Full Range: {full_range}')

            fb = kms.DumbFramebuffer(card, width, height, fmt)

            fb.begin_cpu_access('w')
            kms.testpat.draw_test_pattern(
                fb, pattern=args.pattern, rec_standard=rec_standard, full_range=full_range
            )
            fb.end_cpu_access()

            req = kms.AtomicReq(card)

            req.add_connector(conn, crtc)
            req.add_crtc(crtc, modeb)
            req.add_plane(
                plane,
                fb,
                crtc,
                dst=(0, 0, width, height),
                params={enc_prop_id: rec_standard.value, range_prop_id: full_range.value},
            )

            req.commit_sync(allow_modeset=True)

            old_fb = fb

            input()

    old_fb = None  # noqa: F841


if __name__ == '__main__':
    sys.exit(main())
