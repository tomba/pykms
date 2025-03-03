#!/usr/bin/env python3

import argparse
import numpy as np
import kms

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', default='XRGB8888')
args = parser.parse_args()

format = kms.PixelFormats.find_by_name(args.format)

card = kms.Card()
res = kms.ResourceManager(card)
conn = res.reserve_connector()
crtc = res.reserve_crtc(conn)
mode = conn.get_default_mode()

fb = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, format)

# Example of how to use numpy to modify pixels (XRGB8888/RGB888 only)
map = fb.map(0)

if args.format == 'RGB888':
   b = np.frombuffer(map, dtype=np.uint8).reshape(fb.height, fb.planes[0].pitch // 3, 3)

   # Red square in the top left corner
   b[:fb.height//2, :fb.width//2, :] = [0, 0, 255]

   # Green square in the top right corner
   b[:fb.height//2, fb.width//2:, :] = [0, 255, 0]

   # Blue square in the bottom left corner
   b[fb.height//2:, :fb.width//2, :] = [255, 0, 0]

   # White square in the bottom right corner
   b[fb.height//2:, fb.width//2:, :] = [255, 255, 255]

elif args.format == 'XRGB8888':
   b = np.frombuffer(map, dtype=np.uint8).reshape(fb.height, fb.width, 4)

   # Red square in the top left corner
   b[:fb.height//2, :fb.width//2, :] = [0, 0, 255, 0]

   # Green square in the top right corner
   b[:fb.height//2, fb.width//2:, :] = [0, 255, 0, 0]

   # Blue square in the bottom left corner
   b[fb.height//2:, :fb.width//2, :] = [255, 0, 0, 0]

   # White square in the bottom right corner
   b[fb.height//2:, fb.width//2:, :] = [255, 255, 255, 0]

kms.AtomicReq.set_mode(conn, crtc, fb, mode)

print('Press enter to exit')
input()

# We need to release the numpy array, as it references the mmap
b = None
