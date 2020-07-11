#   Copyright (C) 2020 CyberSIEM (R)
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

import socket
import struct
from telnetlib import Telnet


def tcp(host: str, port: int, payload: bytes) -> int:

    if isinstance(payload, str):
        payload = bytes(payload, 'utf-8')

    with Telnet(host, port) as session:
        session.write(payload)

    return len(payload)


def udp(host: str, port: int, payload: bytes) -> int:

    if isinstance(payload, str):
        payload = bytes(payload, 'utf-8')

    address = host, port
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(payload, address)

    return len(payload)


def multicast(group: str, port: int, payload: bytes) -> int:

    if isinstance(payload, str):
        payload = bytes(payload, 'utf-8')

    return len(payload)


def broadcast(port: int, payload: bytes) -> int:

    if isinstance(payload, str):
        payload = bytes(payload, 'utf-8')

    return len(payload)
