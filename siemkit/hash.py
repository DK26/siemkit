#   Copyright (C) 2020 CyberSIEM(R)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import zlib


def crc32(data):
    return hex(zlib.crc32(data))[2:]


def crc32_file(path, chunk_size=1024):

    total_bytes = 0

    with open(path, "rb") as fs:

        while True:

            byte = fs.read(chunk_size)
            if not byte:
                break

            total_bytes = zlib.crc32(byte, total_bytes)

    return hex(total_bytes & 0xFFFFFFFF)[2:]

