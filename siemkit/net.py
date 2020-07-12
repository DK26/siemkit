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

from typing import Union
from telnetlib import Telnet
from . import send


class WriteableConnectionless:

    def __init__(self, send_function: callable, *args, **kwargs):

        self.send_function = send_function
        self.args = args
        self.kwargs = kwargs

    def write(self, payload: Union[bytes, str]) -> int:
        return self.send_function(*self.args, **self.kwargs, payload=payload)

    def close(self):
        pass  # Do nothing.


def tcp(host: str, port: int = 514, timeout: int = 3) -> Telnet:
    return Telnet(host, port, timeout=timeout)


def udp(host: str, port: int = 514, ttl: int = 32) -> WriteableConnectionless:
    return WriteableConnectionless(send.udp, host=host, port=port, ttl=ttl)


def multicast(group: str, port: int = 514, ttl: int = 2) -> WriteableConnectionless:
    return WriteableConnectionless(send.multicast, group=group, port=port, ttl=ttl)


def broadcast(port: int = 514, ttl: int = 2) -> WriteableConnectionless:
    return WriteableConnectionless(send.broadcast, port=port, ttl=ttl)
