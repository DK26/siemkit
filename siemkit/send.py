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

from telnetlib import Telnet
from typing import Union
from ipaddress import ip_address

default = {
    'unicode': 'utf-8'
}


def tcp(host: str, port: int, payload: Union[bytes, str], timeout: int = 3) -> int:

    if isinstance(payload, str):
        payload = bytes(payload, default['unicode'])

    with Telnet(host, port, timeout=timeout) as session:
        session.write(payload)

    return len(payload)


def udp(host: str, port: int, payload: Union[bytes, str], ttl=32) -> int:

    if isinstance(payload, str):
        payload = bytes(payload, default['unicode'])

    address = host, port
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    udp_socket.sendto(payload, address)

    return len(payload)


def multicast(group: str, port: int, payload: Union[bytes, str], ttl=2) -> int:

    # REF: https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python

    if isinstance(payload, str):
        payload = bytes(payload, default['unicode'])

    if not ip_address(group).is_multicast:
        raise ValueError(f"Address '{group}' is not a multi-cast group.")

    address = group, port
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    multicast_socket.sendto(payload, address)

    return len(payload)


def broadcast(port: int, payload: Union[bytes, str], ttl: int = 1) -> int:

    # REF: https://gist.github.com/ninedraft/7c47282f8b53ac015c1e326fffb664b5

    if isinstance(payload, str):
        payload = bytes(payload, default['unicode'])

    address = '255.255.255.255', port
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, ttl)
    broadcast_socket.sendto(payload, address)

    return len(payload)
