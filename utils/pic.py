#!/usr/bin/env python3

import argparse
from PIL import Image
import numpy as np
import kms

parser = argparse.ArgumentParser()
parser.add_argument('image')
parser.add_argument('-f', '--format', default='XRGB8888')
args = parser.parse_args()

format = kms.PixelFormats.find_by_name(args.format)

card = kms.Card()
res = kms.ResourceManager(card)
conn = res.reserve_connector()
crtc = res.reserve_crtc(conn)
mode = conn.get_default_mode()
fb = kms.DumbFramebuffer(card, mode.hdisplay, mode.vdisplay, format)
kms.AtomicReq.set_mode(conn, crtc, fb, mode)

image = Image.open(args.image)
image = image.resize((mode.hdisplay, mode.vdisplay),
                     Image.Resampling.LANCZOS)
pixels = np.array(image)

map = fb.map(0)
b = np.frombuffer(map, dtype=np.uint8).reshape(fb.height, fb.width, 4)
b[:, :, :] = pixels

print('Press enter to exit')
input()

# We need to release the numpy array, as it references the mmap
b = None
