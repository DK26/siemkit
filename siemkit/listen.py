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

from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Generator
from typing import Tuple

import socket


class ReceiveInterface:
    pass


def udp(ip_address, port, buffer_size=1024) -> Generator[Tuple[bytes, str], None, None]:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((ip_address, port))

    while True:
        yield sock.recvfrom(buffer_size)
