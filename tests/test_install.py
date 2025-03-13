#!/usr/bin/env python3

import unittest
import kms

class TestInstall(unittest.TestCase):
    def test_install(self):
        # Just do something with kms to see it has imported ok
        self.assertEqual(kms.PixelFormats.XRGB8888.drm_fourcc, 0x34325258)

if __name__ == '__main__':
    unittest.main()
