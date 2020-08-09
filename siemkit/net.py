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

from typing import Any
from telnetlib import Telnet
from time import sleep
from abc import ABC
from abc import abstractmethod

from . import send


class WriteableConnection(ABC):

    @abstractmethod
    def write(self, payload: Any) -> int:
        pass

    @abstractmethod
    def close(self):
        pass


class WriteableConnectionless(WriteableConnection):

    def __init__(self, send_function: callable, *args, **kwargs):

        self.send_function = send_function
        self.args = args
        self.kwargs = kwargs

    def write(self, payload: Any) -> int:
        return self.send_function(*self.args, **self.kwargs, payload=payload)

    def close(self):
        pass  # Do nothing.


class TcpConnection(WriteableConnection):

    def __init__(self,
                 host: str,
                 port: int,
                 timeout: int = 3,
                 retries: int = 2,
                 retry_suspense: int = 3
                 ):

        self.__host = host
        self.__port = port
        self.__timeout = timeout
        self.__retries = retries
        self.__retry_suspense = retry_suspense
        self.__session = self.connect()

    def connect(self):

        for attempt in range(self.__retries):
            try:

                return Telnet(
                    self.__host,
                    self.__port,
                    timeout=self.__timeout
                )

            except:

                if attempt + 1 < self.__retries:
                    sleep(self.__retry_suspense)

        raise Exception(f"Unable to establish TCP connection with '{self.__host}:{self.__port}'.")

    def write(self, payload: Any) -> int:

        bytes_payload = send.to_bytes(payload)

        try:
            self.__session.write(bytes_payload)
        except:
            self.__session = self.connect()
            return self.write(bytes_payload)

        return len(bytes_payload)

    def close(self):
        self.__session.close()


def tcp(host: str, port: int = 514, timeout: int = 3, retries: int = 2, retry_suspense: int = 3) -> TcpConnection:
    return TcpConnection(
        host=host,
        port=port,
        timeout=timeout,
        retries=retries,
        retry_suspense=retry_suspense
    )


def udp(host: str, port: int = 514, ttl: int = 32) -> WriteableConnectionless:
    return WriteableConnectionless(send.udp, host=host, port=port, ttl=ttl)


def multicast(group: str, port: int = 514, ttl: int = 2) -> WriteableConnectionless:
    return WriteableConnectionless(send.multicast, group=group, port=port, ttl=ttl)


def broadcast(port: int = 514, ttl: int = 2) -> WriteableConnectionless:
    return WriteableConnectionless(send.broadcast, port=port, ttl=ttl)
