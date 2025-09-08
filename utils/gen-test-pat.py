#!/usr/bin/env python3

import argparse
import sys

import kms


REC_STANDARD_MAP = {
    'bt601': kms.testpat.RecStandard.BT601,
    'bt709': kms.testpat.RecStandard.BT709,
    'bt2020': kms.testpat.RecStandard.BT2020
}

def generate_filename(width, height, format_name, rec_standard=None, full_range=None):
    base = f'{width}x{height}_{format_name}'

    # Add rec standard and range for YUV formats
    if rec_standard is not None and full_range is not None:
        range_str = 'full' if full_range else 'limited'
        return f'{base}_{rec_standard}_{range_str}.raw'

    return f'{base}.raw'

def main():
    parser = argparse.ArgumentParser(description='Generate test patterns as raw image files')
    parser.add_argument('width', type=int,
                        help='Width in pixels')
    parser.add_argument('height', type=int,
                        help='Height in pixels')
    parser.add_argument('format',
                        help='Pixel format name')
    parser.add_argument('-p', '--pattern', default='',
                        help='Test pattern name (default: empty)')
    parser.add_argument('--rec-standard', choices=['bt601', 'bt709', 'bt2020'],
                        default='bt601',
                        help='Recording standard (default: bt601)')
    parser.add_argument('--full-range', action='store_true', default=True,
                        help='Use full range (default: True)')
    parser.add_argument('--no-full-range', dest='full_range', action='store_false',
                        help='Use limited range')

    args = parser.parse_args()

    try:
        format_obj = kms.PixelFormats.find_by_name(args.format)
    except StopIteration:
        print(f"Error: Unknown pixel format '{args.format}'", file=sys.stderr)
        return 1

    # Convert rec standard to enum
    rec_standard_enum = REC_STANDARD_MAP[args.rec_standard]

    # Convert full_range to enum
    full_range_enum = kms.testpat.ColorRange.FULL if args.full_range else kms.testpat.ColorRange.LIMITED

    # Generate filename
    if format_obj.color == kms.PixelColorEncoding.YUV:
        filename = generate_filename(args.width, args.height, args.format,
                                   args.rec_standard, args.full_range)
    else:
        filename = generate_filename(args.width, args.height, args.format)

    try:
        # Create CPU-only framebuffer
        fb = kms.CPUFramebuffer(args.width, args.height, format_obj)

        # Generate test pattern
        kms.testpat.draw_test_pattern(fb, pattern=args.pattern,
                                      rec_standard=rec_standard_enum,
                                      full_range=full_range_enum)

        # Write raw data to file
        with open(filename, 'wb') as f:
            for plane_idx in range(len(fb.planes)):
                mapped_data = fb.map(plane_idx)
                f.write(mapped_data)

        print(f'Generated: {filename}')

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
