#!/usr/bin/env python3

import os
import pprint

import pyudev

import kms

card = kms.Card()
card_name = os.path.basename(card.dev_path)

context = pyudev.Context()

monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('drm')

for device in iter(monitor.poll, None):
    if device.sys_name != card_name or 'HOTPLUG' not in device:
        continue

    print('== HPD ==')
    for conn in card.connectors:
        conn.refresh()
        strs = (
            conn.fullname,
            'connected' if conn.connected else 'disconnected',
            [f'{m.hdisplay}x{m.vdisplay}' for m in conn.modes],
        )
        pprint.pprint(strs, compact=True, width=120)
