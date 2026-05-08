#!/usr/bin/env python3

"""Generate test patterns as raw image files using pixpat."""

import argparse
import sys

import pixpat
from pixutils.formats import PixelFormats, PixelColorEncoding


REC_MAP = {
    'bt601': pixpat.Rec.BT601,
    'bt709': pixpat.Rec.BT709,
    'bt2020': pixpat.Rec.BT2020,
}


def parse_param(s):
    if '=' not in s:
        raise argparse.ArgumentTypeError(f"--param must be 'key=value', got: {s!r}")
    key, value = s.split('=', 1)
    return key, value


def generate_filename(width, height, format_name, rec_standard=None, full_range=None):
    base = f'{width}x{height}_{format_name}'
    if rec_standard is not None and full_range is not None:
        range_str = 'full' if full_range else 'limited'
        return f'{base}_{rec_standard}_{range_str}.raw'
    return f'{base}.raw'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('width', type=int, help='Width in pixels')
    parser.add_argument('height', type=int, help='Height in pixels')
    parser.add_argument('format', help='Pixel format name (e.g. XRGB8888, NV12)')
    parser.add_argument('-p', '--pattern', default=None,
                        help='Pattern name; see pixpat.draw_pattern for the list. '
                             'Default: pixpat default (kmstest)')
    parser.add_argument('--param', dest='params', type=parse_param, action='append',
                        default=[], metavar='KEY=VALUE',
                        help='Pattern-specific parameter; may be repeated. '
                             'See pixpat.draw_pattern for per-pattern keys '
                             "(e.g. 'color=ff0000' for plain, 'cell=16' for checker).")
    parser.add_argument('--rec-standard', choices=['bt601', 'bt709', 'bt2020'],
                        default='bt601',
                        help='YCbCr matrix for YUV formats (default: bt601)')
    parser.add_argument('--full-range', action='store_true', default=True,
                        help='Use full quantization range for YUV (default)')
    parser.add_argument('--no-full-range', dest='full_range', action='store_false',
                        help='Use limited quantization range for YUV')

    args = parser.parse_args()

    try:
        format_obj = PixelFormats.find_by_name(args.format)
    except StopIteration:
        print(f"Error: Unknown pixel format '{args.format}'", file=sys.stderr)
        return 1

    aligned_width, aligned_height = format_obj.align_pixels(args.width, args.height)

    planes = []
    strides = []
    for plane_idx in range(len(format_obj.planes)):
        stride = format_obj.stride(aligned_width, plane_idx)
        size = format_obj.planesize(stride, aligned_height, plane_idx)
        planes.append(bytearray(size))
        strides.append(stride)

    rec = REC_MAP[args.rec_standard]
    color_range = pixpat.Range.FULL if args.full_range else pixpat.Range.LIMITED

    buf = pixpat.Buffer(planes=planes, fmt=args.format,
                        width=args.width, height=args.height,
                        strides=strides)

    params = dict(args.params) if args.params else None

    try:
        pixpat.draw_pattern(buf, args.pattern, rec=rec, color_range=color_range,
                            params=params)
    except (pixpat.PixpatError, ValueError, TypeError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

    if format_obj.color == PixelColorEncoding.YUV:
        filename = generate_filename(args.width, args.height, args.format,
                                     args.rec_standard, args.full_range)
    else:
        filename = generate_filename(args.width, args.height, args.format)

    with open(filename, 'wb') as f:
        for plane_data in planes:
            f.write(plane_data)

    print(f'Generated: {filename}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
