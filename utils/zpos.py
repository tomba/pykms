#!/usr/bin/env python3

import atexit
import sys
import kms
from kms import drawing

def exit_handler():
    print('Press enter to exit program')
    sys.stdin.readline()

atexit.register(exit_handler)

card = kms.Card()
res = kms.ResourceManager(card)

dp = res.reserve_connector('dp')
dp_crtc = res.reserve_crtc(dp)
dp_mode = dp.get_default_mode()
dp_modeb = dp_mode.to_blob(card)

hdmi = res.reserve_connector('hdmi')
hdmi_crtc = res.reserve_crtc(hdmi)
hdmi_mode = hdmi.get_default_mode()
hdmi_modeb = hdmi_mode.to_blob(card)

p1 = res.reserve_generic_plane(dp_crtc)
p2 = res.reserve_generic_plane(dp_crtc)
p3 = res.reserve_generic_plane(hdmi_crtc)
p4 = res.reserve_generic_plane(hdmi_crtc)
planes = [p1, p2, p3, p4]

w = 500
h = 500

fbs=[]

for i in range(len(planes)):
    fb = kms.DumbFramebuffer(card, w, h, kms.PixelFormats.ARGB8888)
    fbs.append(drawing.NumpyFramebuffer(fb))

fbs[0].fill_rect(50, 50, 200, 200, drawing.RGB(128, 255, 0, 0))
fbs[1].fill_rect(150, 50, 200, 200, drawing.RGB(128, 0, 255, 0))
fbs[2].fill_rect(50, 150, 200, 200, drawing.RGB(128, 0, 0, 255))
fbs[3].fill_rect(150, 150, 200, 200, drawing.RGB(128, 128, 128, 128))

req = kms.AtomicReq(card)

req.add_connector(dp, dp_crtc)
req.add_crtc(dp_crtc, dp_modeb)

req.add_connector(hdmi, hdmi_crtc)
req.add_crtc(hdmi_crtc, hdmi_modeb)

req.add_plane(planes[0], fbs[0], dp_crtc, zpos=0)
req.add_plane(planes[1], fbs[1], dp_crtc, zpos=0)
req.add_plane(planes[2], fbs[2], hdmi_crtc, zpos=0)
req.add_plane(planes[3], fbs[3], hdmi_crtc, zpos=0)

req.commit_sync(allow_modeset = True)



def setz(p: kms.Plane, z: int):
    p.set_prop('zpos', z)

def pr():
    for p in planes:
        p.refresh_props()
        print(f'{p.idx}: {p.plane_type}, zpos = {p.get_prop_value("zpos")}')

pr()


print('press enter'); sys.stdin.readline()

#req = kms.AtomicReq(card)
#req.add(dp_crtc, 'ACTIVE', 0)
#req.add(hdmi_crtc, 'ACTIVE', 0)
#req.commit_sync(allow_modeset = True)
#print("press enter"); sys.stdin.readline()

req = kms.AtomicReq(card)
req.add_plane(planes[0], None, None)
req.add_plane(planes[1], None, None)
req.add_plane(planes[2], None, None)
req.add_plane(planes[3], None, None)
req.commit_sync(allow_modeset = False)
print('press enter'); sys.stdin.readline()


req = kms.AtomicReq(card)

req.add_plane(planes[0], fbs[0], hdmi_crtc, zpos=0)
req.add_plane(planes[1], fbs[1], hdmi_crtc, zpos=0)
req.add_plane(planes[2], fbs[2], dp_crtc, zpos=0)
req.add_plane(planes[3], fbs[3], dp_crtc, zpos=0)

req.commit_sync(allow_modeset = False)
print('press enter'); sys.stdin.readline()

#req = kms.AtomicReq(card)
##req.add(dp_crtc, 'ACTIVE', 1)
##req.add(hdmi_crtc, 'ACTIVE', 1)
#req.add_plane(planes[0], fbs[0], hdmi_crtc, zpos=0)
##req.add_plane(planes[1], fbs[1], hdmi_crtc, zpos=0)
##req.add_plane(planes[2], fbs[2], dp_crtc, zpos=0)
##req.add_plane(planes[3], fbs[3], dp_crtc, zpos=0)
#req.commit_sync(allow_modeset = False)
#print("press enter"); sys.stdin.readline()


#import IPython
#IPython.embed(banner1='', confirm_exit=False)
