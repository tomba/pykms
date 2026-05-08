from __future__ import annotations

import pixpat

import kms

__all__ = ['draw_test_pattern', 'pixpat_buffer']


def pixpat_buffer(fb: kms.IFramebuffer) -> pixpat.Buffer:
    """Wrap a pykms framebuffer as a :class:`pixpat.Buffer`.

    Use this when you want to call :func:`pixpat.draw_pattern` directly to
    pass pattern-specific ``params`` or other options that
    :func:`draw_test_pattern` does not expose.
    """
    return pixpat.Buffer(
        planes=fb.mmap(),
        fmt=fb.format.name,
        width=fb.width,
        height=fb.height,
        strides=[p.pitch for p in fb.planes],
    )


def draw_test_pattern(fb: kms.IFramebuffer, pattern: str | None = None,
                      rec: pixpat.Rec = pixpat.Rec.BT601,
                      color_range: pixpat.Range = pixpat.Range.FULL) -> None:
    """Draw a test pattern into ``fb`` using :func:`pixpat.draw_pattern`.

    Convenience one-liner. For per-pattern ``params`` or other customization,
    call :func:`pixpat.draw_pattern` directly with :func:`pixpat_buffer`.

    Args:
        fb: Destination framebuffer; all planes must be CPU-writable.
        pattern: Pattern name. ``None`` selects pixpat's default
            (``"kmstest"``). See :func:`pixpat.draw_pattern`.
        rec: YCbCr matrix used for YUV outputs (ignored for RGB / raw).
        color_range: Quantization range used for YUV outputs (ignored for
            RGB / raw).
    """
    pixpat.draw_pattern(pixpat_buffer(fb), pattern, rec=rec, color_range=color_range)
