#!/usr/bin/env python3

import argparse
import re
import sys

import kms

def printi(indent: int, *args):
    print(' ' * indent, end='')
    print(*args)

class Printer:
    def __init__(self, args: argparse.Namespace) -> None:
        self.opt_print_props = args.props
        self.opt_prop_filter = args.prop_filter

        if self.opt_prop_filter:
            self.opt_print_props = True

    def print_props(self, o: kms.DrmPropObject, indent: int):
        if not self.opt_print_props:
            return

        for p,val in o.props:
            if self.opt_prop_filter and not re.match(self.opt_prop_filter, p.name):
                continue
            printi(indent, f'{p.name}: {val}')

    def print_connector(self, c: kms.Connector, indent: int):
        printi(indent, f'Connector {c.idx} ({c.id}) {c.fullname} ({"connected" if c.connected else "disconnected"})')
        self.print_props(c, indent + 4)

    def print_encoder(self, e: kms.Encoder, indent: int):
        printi(indent, f'Encoder {e.idx} ({e.id}) {e.encoder_type.name}')

    def print_crtc(self, crtc: kms.Crtc, indent: int):
        m = crtc.mode

        refresh = (m.clock * 1000.0) / (m.htotal * m.vtotal) * (2 if m.interlace else 1)
        refresh = round(refresh, 2)

        printi(indent, f'Crtc {crtc.idx} ({crtc.id}) {m.hdisplay}x{m.vdisplay}@{refresh} {m.clock / 1000:.3f}')

        self.print_props(crtc, indent + 4)

    def print_plane(self, p: kms.Plane, indent: int):
        src_x = p.get_prop_value('SRC_X') >> 16
        src_y = p.get_prop_value('SRC_Y') >> 16
        src_w = p.get_prop_value('SRC_W') >> 16
        src_h = p.get_prop_value('SRC_H') >> 16

        crtc_x = p.get_prop_value('CRTC_X')
        crtc_y = p.get_prop_value('CRTC_Y')
        crtc_w = p.get_prop_value('CRTC_W')
        crtc_h = p.get_prop_value('CRTC_H')

        printi(indent, f'Plane {p.idx} ({p.id}) fb-id {p.fb_id} ' +
              f'{src_x},{src_y} {src_w}x{src_h} -> {crtc_x},{crtc_y} {crtc_w}x{crtc_h} ')

        self.print_props(p, indent + 4)

    def print_fb(self, fb: kms.Framebuffer, indent: int):
        printi(indent, f'FB ({fb.id}) {fb.width}x{fb.height} {fb.format.name} pixel_align={fb.format.pixel_align} ')

        for idx, p in enumerate(fb.planes):
            pi = fb.format.planes[idx]
            printi(indent + 2, f'Plane {idx}: offset={p.offset} pitch={p.pitch} size={p.size} bytes_per_block={pi.bytes_per_block} pixels_per_block={pi.pixels_per_block} hsub={pi.hsub} vsub={pi.vsub}')

    def print_card(self, card: kms.Card):
        ver = card.get_version()
        printi(0, f'Node: {card.dev_path} Driver: {ver.name} {ver.date} {ver.desc}')

        for c in card.connectors:
            self.print_connector(c, 2)

            for e in c.encoders:
                self.print_encoder(e, 4)

                crtc = e.crtc

                if not crtc:
                    continue

                self.print_crtc(crtc, 6)

                for p in card.planes:
                    if p.crtc_id != crtc.id:
                        continue

                    self.print_plane(p, 8)

                    if p.fb_id:
                        fb = card.get_framebuffer(p.fb_id)
                        self.print_fb(fb, 10)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--props', action='store_true')
    parser.add_argument('-f', '--prop-filter', default='')
    args = parser.parse_args()

    if args.prop_filter:
        args.prop_filter = re.compile(args.prop_filter)

    printer = Printer(args)

    card = kms.Card()
    printer.print_card(card)


if __name__ == '__main__':
    sys.exit(main())
