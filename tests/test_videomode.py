#!/usr/bin/env python3

import unittest

import kms


def mode_1080p():
    m = kms.VideoMode()
    m.clock = 148500000
    m.hdisplay = 1920
    m.hfp = 88
    m.hsw = 44
    m.hbp = 148
    m.vdisplay = 1080
    m.vfp = 4
    m.vsw = 5
    m.vbp = 36
    m.vrefresh = 60
    m.flags = kms.ModeFlag.HSYNC_POS | kms.ModeFlag.VSYNC_POS
    m.type = kms.ModeType.DRIVER | kms.ModeType.PREFERRED
    m.name = '1920x1080'
    return m


class TestVideoMode(unittest.TestCase):
    def test_timings(self):
        m = mode_1080p()

        self.assertEqual(m.hsync_start, 2008)
        self.assertEqual(m.hsync_end, 2052)
        self.assertEqual(m.htotal, 2200)
        self.assertEqual(m.vsync_start, 1084)
        self.assertEqual(m.vsync_end, 1089)
        self.assertEqual(m.vtotal, 1125)

    def test_polarity(self):
        m = mode_1080p()

        self.assertEqual(m.hsync_polarity, 1)
        self.assertEqual(m.vsync_polarity, 1)
        self.assertFalse(m.interlace)

        m.flags = kms.ModeFlag.HSYNC_NEG
        self.assertEqual(m.hsync_polarity, -1)
        self.assertEqual(m.vsync_polarity, 0)

    def test_vrefresh(self):
        m = mode_1080p()
        self.assertAlmostEqual(m.calculated_vrefresh, 60.0, places=3)

    def test_vrefresh_interlace(self):
        m = mode_1080p()
        m.clock = 74250000
        m.flags |= kms.ModeFlag.INTERLACE
        self.assertAlmostEqual(m.calculated_vrefresh, 60.0, places=3)

    def test_vrefresh_dblscan(self):
        m = mode_1080p()
        m.flags |= kms.ModeFlag.DBLSCAN
        self.assertAlmostEqual(m.calculated_vrefresh, 30.0, places=3)

    def test_vrefresh_vscan(self):
        m = mode_1080p()
        m.vscan = 2
        self.assertAlmostEqual(m.calculated_vrefresh, 30.0, places=3)

    def test_empty_mode(self):
        m = kms.VideoMode()
        self.assertEqual(m.calculated_vrefresh, 0)
        # Must not raise
        m.to_str()
        m.to_str_modeline()

    def test_modeinfo_roundtrip(self):
        m = mode_1080p()
        m2 = kms.VideoMode._from_modeinfo(m._to_modeinfo())
        self.assertEqual(m.__dict__, m2.__dict__)

    def test_copy(self):
        m = mode_1080p()
        m2 = m.copy()
        self.assertEqual(m.__dict__, m2.__dict__)
        m2.hdisplay = 1280
        self.assertEqual(m.hdisplay, 1920)


if __name__ == '__main__':
    unittest.main()
