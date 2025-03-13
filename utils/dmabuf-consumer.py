#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

import os
import socket
import struct
import sys
import time

# Constants
SOCKET_PATH = '/tmp/dmabuf_socket'

@dataclass
class FramebufferSource:
    framebuffers: list[tuple]
    free_fbs: list[int]

def recv_ints(sock, num_ints):
    data, ancdata, flags, addr = sock.recvmsg(struct.calcsize(f'{num_ints}i'))
    if not data:
        print('recvmsg returned no data')
        sys.exit(1)
    return struct.unpack(f'{num_ints}i', data)

def main():
    # Create a Unix domain socket
    client_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_sock.connect(SOCKET_PATH)

    sources = []
    num_sources = recv_ints(client_sock, 1)[0]

    for src_id in range(num_sources):
        num_fbs = recv_ints(client_sock, 1)[0]
        framebuffers = []
        for i in range(num_fbs):
            data, fds, flags, addr = socket.recv_fds(client_sock, struct.calcsize('iiiiiii'), 1)
            fb_id, xxx_fd, fb_size, fb_format, width, height, stride = struct.unpack('iiiiiii', data)
            fd = fds[0]
            framebuffers.append((fb_id, fd, fb_size, fb_format, width, height))
            print(f'Received source {src_id} framebuffer metadata and fd {fd} with id {fb_id}')
        sources.append(FramebufferSource(framebuffers, []))

    while True:
        data = recv_ints(client_sock, 2)

        src_id, fb_id = data
        print(f'Src{src_id} framebuffer with id {fb_id} received')

        # Check if the file descriptor is still valid
        def is_fd_valid(fd):
            try:
                os.fstat(fd)
            except OSError:
                return False
            return True

        # Find the framebuffer with the given id
        fb_tuple = sources[src_id].framebuffers[fb_id]

        if is_fd_valid(fb_tuple[1]):
            print(f'Framebuffer with id {fb_id} has a valid fd {fb_tuple[1]}')
        else:
            print(f'Framebuffer with id {fb_id} has an invalid fd {fb_tuple[1]}')

        time.sleep(0.01)

        client_sock.sendmsg([struct.pack('ii', src_id, fb_id)])
        print(f'Src{src_id} returned framebuffer with id {fb_id}')

    client_sock.close()
    print('end')

if __name__ == '__main__':
    main()
