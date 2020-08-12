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

from ipaddress import IPv4Address
from typing import Generator


def ip(start, end=None, amount=1) -> Generator[IPv4Address, None, None]:

    if end is None and amount > 0:
        start_ip = int(IPv4Address(start))
        end_ip = start_ip + (amount - 1)
    else:
        start_ip = int(IPv4Address(start))
        end_ip = int(IPv4Address(end))

    for decimal_ip in range(start_ip, end_ip + 1):
        yield IPv4Address(decimal_ip)

