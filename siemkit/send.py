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

import socket

from math import floor

from telnetlib import Telnet
from typing import Any
from ipaddress import ip_address

from siemkit.smtp import AUTH_MODULE_FACTORY as SMTP_AUTH_MODULE_FACTORY
from siemkit.smtp import Connection as SmtpConnection
from siemkit.smtp import MultipartMimeMessage

default = {
    'unicode': 'utf-8',
    'byte_order': 'big',
    'signed': False
}


def to_bytes(payload: Any):

    if isinstance(payload, bytes):
        return payload

    elif callable(payload):
        return to_bytes(payload())

    elif isinstance(payload, str):
        return bytes(payload, default['unicode'])

    elif isinstance(payload, int):

        # Calculate how many bytes are required for given integer.
        bytes_size = floor(payload / 256) + 1

        # Notice: From the int value of 768 (4 bytes),
        # it is more size efficient to send this number or bigger as a string (3 bytes)

        return int.to_bytes(
            payload,
            bytes_size,
            byteorder=default['byte_order'],
            signed=default['signed']
        )

    else:
        return bytes(payload)


def tcp(host: str, port: int, payload: Any, repeat: int = 1, timeout: int = 3) -> int:

    bytes_payload = to_bytes(payload)

    with Telnet(host, port, timeout=timeout) as session:
        for iteration in range(repeat):
            session.write(bytes_payload)

        if iteration + 1 < repeat and callable(payload):
            bytes_payload = to_bytes(payload)

    return len(bytes_payload)


def udp(host: str, port: int, payload: Any, repeat: int = 1, ttl: int = 32) -> int:

    bytes_payload = to_bytes(payload)

    for iteration in range(repeat):

        address = host, port
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        udp_socket.sendto(bytes_payload, address)

        if iteration + 1 < repeat and callable(payload):
            bytes_payload = to_bytes(payload)

    return len(bytes_payload)


def multicast(group: str, port: int, payload: Any, ttl: int = 2) -> int:

    # REF: https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python

    bytes_payload = to_bytes(payload)

    if not ip_address(group).is_multicast:
        raise ValueError(f"Address '{group}' is not a multi-cast group.")

    address = group, port
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    multicast_socket.sendto(bytes_payload, address)

    return len(bytes_payload)


def broadcast(port: int, payload: Any, ttl: int = 1) -> int:

    # REF: https://gist.github.com/ninedraft/7c47282f8b53ac015c1e326fffb664b5

    bytes_payload = to_bytes(payload)

    address = '255.255.255.255', port
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, ttl)
    broadcast_socket.sendto(bytes_payload, address)

    return len(bytes_payload)


def smtp(
        server,
        from_address,
        to_addresses,
        cc_addresses=None,
        bcc_addresses=None,
        subject='',
        content=None,
        content_render=None,
        content_variables=None,
        work_dir=None,
        attachments=None,
        auth_module='tls',
        username=None,
        password=None,
        port=None,
        encoding='utf-8'
):

    if not isinstance(port, int):

        if ':' in server:

            server, port = server.split(':')

            if port != '':
                port = int(port)

        if not port:
            port = {
                'starttls': 587,
                'tls': 465
            }.get(auth_module, 25)

    smtp_auth = SMTP_AUTH_MODULE_FACTORY.create(
        module_name=auth_module,
        server=server,
        port=port,
        username=username,
        password=password,
    )
    SmtpConnection(smtp_auth).sendmail(
        MultipartMimeMessage(
            from_address=from_address,
            to_addresses=to_addresses,
            cc_addresses=cc_addresses,
            bcc_addresses=bcc_addresses,
            subject=subject,
            content=content,
            content_render=content_render,
            content_variables=content_variables,
            work_dir=work_dir,
            attachments=attachments,
            encoding=encoding
        )
    )
