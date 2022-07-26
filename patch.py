#!/usr/bin/env python3
import sys
import os.path
import hashlib

class Patchset():
    def __init__(self, patch_steam):
        self.sha256 = patch_steam.readline().strip("\r\n")
        self.patches = {}
        for x in patch_steam.readlines():
            data = x.split(':')
            if len(data) < 2:
                continue

            offset = int(data[0], 16)
            byte = bytes([int(data[1], 16)])

            self.patches[offset] = byte

    def patch(self, stream):
        for offset, byte in self.patches.items():
            print(f'offset = {offset}, byte = {byte}')
            stream.seek(offset)
            stream.write(byte)

    def sha256_ok(self, stream):
        return hashlib.sha256(stream.read()).hexdigest() == self.sha256

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} file patch')
        exit(1)

    for x in range(3):
        if not os.path.isfile(sys.argv[x]):
            raise FileNotFoundError(sys.argv[x])

    target = sys.argv[1]
    patch = sys.argv[2]

    with open(patch, 'r') as pf:
        ps = Patchset(pf)

    with open(target, 'r+b') as tf:
        if not ps.sha256_ok(tf):
            raise Exception('Provided file is not valid for the specified patch')

        ps.patch(tf)
