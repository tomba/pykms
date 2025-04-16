#!/usr/bin/env python3

import argparse
import select
import sys
import time
import kms

parser = argparse.ArgumentParser(description='Test display clocks for a KMS device')
parser.add_argument('-c', '--connector', help='Specify the connector to use (default: auto-select)')
parser.add_argument('-s', '--start', help='Starting pixel clock frequency (can use MHz/KHz suffix)')
parser.add_argument('-e', '--end', help='Ending pixel clock frequency (can use MHz/KHz suffix)')
parser.add_argument('-i', '--increment', help='Frequency increment step size (can use MHz/KHz suffix)')
parser.add_argument('-t', '--time', type=float, help='Time in seconds to test each frequency')
args = parser.parse_args()

def parse_freq(freq_str):
    if freq_str is None:
        return None

    freq_str = str(freq_str).strip().lower()

    if freq_str.endswith('mhz'):
        return int(float(freq_str.replace('mhz', '')) * 1000 * 1000)
    elif freq_str.endswith('khz'):
        return int(float(freq_str.replace('khz', '')) * 1000)
    else:
        return int(freq_str)

args.start = parse_freq(args.start)
args.end = parse_freq(args.end)
args.increment = parse_freq(args.increment)

card = kms.Card()

res = kms.ResourceManager(card)
conn = res.reserve_connector(args.connector)
crtc = res.reserve_crtc(conn)
plane = res.reserve_generic_plane(crtc)

kms.AtomicReq.disable_all(card)

mode = conn.get_default_mode()

start = args.start if args.start else mode.clock
end = args.end if args.end else mode.clock
increment = args.increment if args.increment else 1000

fb = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, kms.PixelFormats.XRGB8888)
kms.draw_test_pattern(fb)

for pclk in range(start, end + 1, increment):
    mode.clock = pclk
    print(mode.to_str())

    kms.AtomicReq.set_mode(conn, crtc, fb, mode, plane)

    req = kms.AtomicReq(card)
    req.add_plane(plane, fb, crtc)
    req.commit_sync(allow_modeset=False)

    tstart = tlast = time.monotonic()
    frames = 0
    break_loop = False
    break_outer = False
    while not break_loop:
        req = kms.AtomicReq(card)
        req.add_plane(plane, fb, crtc)
        req.commit_sync(allow_modeset=False)
        frames += 1

        tnow = time.monotonic()

        if select.select([sys.stdin], [], [], 0.0)[0]:
            break_loop = True
            if sys.stdin.readline().strip():
                break_outer = True

        if args.time:
            if tnow - tstart >= args.time:
                break_loop = True

        if break_loop or tnow - tlast >= 0.1:
            td = tnow - tstart
            print(f'fps: {frames / td:.2f} ({frames} frames in {td:.2f}s)', end='\r')
            tlast = tnow

        if break_loop:
            if args.time:
                print()
            break

    if break_outer:
        break

print('done')
