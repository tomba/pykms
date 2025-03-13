#!/usr/bin/env python3

import fcntl
import gc
import unittest

import kms


class TestCardMethods(unittest.TestCase):
    def _get_card(self):
        try:
            card = kms.Card()
        except FileNotFoundError as e:
            self.skipTest(e)
        except NotImplementedError as e:
            self.skipTest(e)

        return card

    def test_card(self):
        card = self._get_card()

        fd = card.fd

        card = None
        gc.collect()
        with self.assertRaises(Exception):
            fcntl.fcntl(fd, fcntl.F_GETFD)

    def test_card_fb_2(self):
        card = self._get_card()
        fd = card.fd

        fb = kms.DumbFramebuffer(card, 640, 480, kms.PixelFormats.XRGB8888)

        map = fb.map(0)
        fb_fd = fb.fd(0)
        fcntl.fcntl(fb_fd, fcntl.F_GETFD)

        card = None
        gc.collect()
        fb = None
        gc.collect()
        with self.assertRaises(Exception):
            fcntl.fcntl(fd, fcntl.F_GETFD)
        with self.assertRaises(Exception):
            fcntl.fcntl(fb_fd, fcntl.F_GETFD)
        self.assertTrue(map.closed)


if __name__ == '__main__':
    unittest.main()
