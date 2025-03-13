#!/usr/bin/env python3

import pprint
import pyudev

import kms

card = kms.Card()
connectors = card.connectors

context = pyudev.Context()

dev = pyudev.Devices.from_name(context, 'drm', 'card0')

monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('drm')

for device in iter(monitor.poll, None):
    if 'HOTPLUG' in device:
        print('== HPD ==')
        for conn in connectors:
            conn.refresh_modes()
            strs = (conn.fullname,
                    ['{}x{}'.format(m.hdisplay, m.vdisplay) for m in conn.modes])
            pprint.pprint(strs, compact=True, width=120)
