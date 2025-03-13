#!/usr/bin/env python3

from __future__ import annotations

import os
import select
import socket
import struct
import time

from kms import Card, PixelFormats
from kms.framebuffer import DumbFramebuffer
import numpy as np

# Constants
SOCKET_PATH = '/tmp/dmabuf_socket'
SOURCE_COUNT = 1
FRAMEBUFFER_COUNT = 5
FRAMEBUFFER_WIDTH = 640
FRAMEBUFFER_HEIGHT = 480
FRAMEBUFFER_FORMAT = PixelFormats.XRGB8888
FRAME_INTERVAL = 1 / 10

def fill_random(fb: DumbFramebuffer):
    fb.begin_cpu_access('rw')

    random_data = np.random.randint(0, 256, (fb.height, fb.planes[0].pitch), dtype=np.uint8)
    buf = np.frombuffer(fb.map(0), dtype=np.dtype(np.uint8))
    buf[:] = random_data

    fb.end_cpu_access()

def draw_line(fb: DumbFramebuffer, y: int):
    fb.begin_cpu_access('rw')

    buf = np.frombuffer(fb.map(0), dtype=np.dtype(np.uint8))
    buf = buf.reshape((fb.height, fb.planes[0].pitch))

    # Clear the framebuffer
    buf[:] = 0
    buf[y, :] = 255

    fb.end_cpu_access()

class FramebufferSource:
    framebuffers: list[DumbFramebuffer]
    free_fbs: list[int]
    sent_fbs: list[int]

    def __init__(self, framebuffers, free_fbs):
        self.framebuffers = framebuffers
        self.free_fbs = free_fbs
        self.sent_fbs = []

def main():
    card = Card()

    sources = []

    for src_id in range(SOURCE_COUNT):
        framebuffers = []
        for fb_id in range(FRAMEBUFFER_COUNT):
            fb = DumbFramebuffer(card, FRAMEBUFFER_WIDTH, FRAMEBUFFER_HEIGHT, FRAMEBUFFER_FORMAT)
            draw_line(fb, 300)
            framebuffers.append(fb)
        sources.append(FramebufferSource(framebuffers, list(range(FRAMEBUFFER_COUNT))))

    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_sock.bind(SOCKET_PATH)

    server_sock.listen(1)

    print('Waiting for a connection...')
    client, src_id = server_sock.accept()
    print('Client connected')

    # Send number of sources
    client.sendmsg([struct.pack('i', len(sources))])
    for src_id, src in enumerate(sources):
        # Send number of framebuffers
        client.sendmsg([struct.pack('i', len(src.framebuffers))])

        # Send framebuffer metadata to consumer
        for fb_id, fb in enumerate(src.framebuffers):
            fb_fd = fb.fd(0)
            metadata = struct.pack('iiiiiii', fb_id, fb_fd, fb.size(0), fb.format.drm_fourcc,
                                fb.width, fb.height, fb.planes[0].pitch)
            socket.send_fds(client, [metadata], [fb_fd])
            print(f'Sent framebuffer metadata and fd {fb_fd} with id {fb_id}')

    # Send one framebuffer from each source to consumer as initial fb
    for src_id, src in enumerate(sources):
        fb_id = src.free_fbs.pop(0)
        src.sent_fbs.append(fb_id)
        client.sendmsg([struct.pack('ii', src_id, fb_id)])
        print(f'Src{src_id} queued framebuffer with id {fb_id}, line 300')

    line = 0
    last_frame_time = time.monotonic()

    try:
        while True:
            now = time.monotonic()

            # Check for returned framebuffers
            while True:
                ready = select.select([client], [], [], 0)
                if ready[0]:
                    data, ancdata, flags, addr = client.recvmsg(struct.calcsize('ii'))
                    if data:
                        src_id, fb_id = struct.unpack('ii', data)
                        src = sources[src_id]

                        assert fb_id not in src.free_fbs
                        src.free_fbs.append(fb_id)

                        assert fb_id in src.sent_fbs
                        src.sent_fbs.remove(fb_id)

                        print(f'Src{src_id} framebuffer {fb_id} returned. Free fbs {len(src.free_fbs)}')

                        # Fill received fb with random data, to see that the consumer is not using it
                        fill_random(src.framebuffers[fb_id])
                    else:
                        print('Client disconnected')
                        return
                else:
                    break

            # Time to send a new frame?
            if now >= last_frame_time + FRAME_INTERVAL:
                line = (line + 1) % FRAMEBUFFER_HEIGHT

                for src_id, src in enumerate(sources):
                    free_fbs = src.free_fbs
                    if not free_fbs:
                        print('No free framebuffers')
                        continue

                    fb_id = free_fbs.pop(0)

                    assert fb_id not in src.sent_fbs
                    src.sent_fbs.append(fb_id)

                    # Draw a line on the framebuffer
                    draw_line(src.framebuffers[fb_id], line)

                    # Queue framebuffer to consumer
                    client.sendmsg([struct.pack('ii', src_id, fb_id)])
                    print(f'Src{src_id} queued framebuffer with id {fb_id}, line {line}')

                last_frame_time = now

    except KeyboardInterrupt:
        print('\nShutting down...')
    finally:
        server_sock.close()
        os.remove(SOCKET_PATH)


if __name__ == '__main__':
    main()
