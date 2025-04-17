from __future__ import annotations

import ctypes
import kms

__all__ = [ 'draw_test_pattern', ]

class CDrawTestPatternParameters(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_uint32),
        ('height', ctypes.c_uint32),
        ('fourcc', ctypes.c_uint32),
        ('buffers', ctypes.POINTER(ctypes.c_uint8) * 4),
        ('sizes', ctypes.c_uint32 * 4),
        ('pitches', ctypes.c_uint32 * 4),
        ('offsets', ctypes.c_uint32 * 4),

        ('pattern', ctypes.c_char_p),
        ('rec_standard', ctypes.c_uint32),
        ('full_range', ctypes.c_bool),
    ]

def draw_test_pattern(fb: kms.Framebuffer, pattern: str='',
                      rec_standard: int=0, full_range: bool=True) -> None:
    """WARNING: Experimental, unstable! The C API might change, breaking this"""
    try:
        dll = ctypes.cdll.LoadLibrary('libkms++util.so')

        c_draw_test_pattern = dll.c_draw_test_pattern
        if not c_draw_test_pattern:
            raise Exception('Native c_draw_test_pattern() not found')
    except Exception as e:
        print(f'No native c_draw_test_pattern() found: {e}')
        return

    opts = CDrawTestPatternParameters()
    opts.width = fb.width
    opts.height = fb.height
    opts.fourcc = fb.format.drm_fourcc

    # This is a bit silly way to get the pointer of the memory map, but I did
    # not find out a direct way.
    l = []
    for buffer in fb.mmap():
        first_byte = ctypes.c_uint8.from_buffer(buffer)
        p_first_byte = ctypes.cast(ctypes.addressof(first_byte), ctypes.POINTER(ctypes.c_uint8))
        l.append(p_first_byte)

    opts.buffers = (ctypes.POINTER(ctypes.c_uint8) * 4)(*l)
    opts.sizes = (ctypes.c_uint32 * 4)(*[p.size for p in fb.planes])
    opts.pitches = (ctypes.c_uint32 * 4)(*[p.pitch for p in fb.planes])
    opts.offsets = (ctypes.c_uint32 * 4)(*[p.offset for p in fb.planes])
    opts.pattern = pattern.encode('utf-8')
    opts.rec_standard = rec_standard
    opts.full_range = full_range

    c_draw_test_pattern(ctypes.byref(opts))
