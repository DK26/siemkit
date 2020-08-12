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

from typing import Generator

from siemkit.event import Cef
from siemkit.time import sleep
from siemkit import random
from siemkit import generate
from random import randint


def random_number(start_range: int = None, end_range: int = None, amount: int = 1, event: Cef = None) \
        -> Generator[Cef, None, None]:
    """
    Simulate for aggregation test by producing a random number value in `deviceCustomNumber1`
    :param start_range:
    :param end_range:
    :param amount:
    :param event: Optional CEF event to work with. The CEF original state is kept protected.
    :return:
    """

    if amount < 1:
        amount = 1

    if end_range is None and isinstance(start_range, int) and start_range >= 0:
        end_range = start_range
        start_range = 0

    if start_range is None and end_range is None:
        start_range = 0
        end_range = 4

    if event is None:
        event = Cef()

    with event:
        for _ in range(amount):
            event.deviceCustomNumber1 = randint(start_range, end_range)
            yield event


def fake_ip_scan(event: Cef = None) -> Generator[Cef, None, None]:
    """
    Simulate a fake IP scan & telnet login.

    Steps:

        1. Pick a random attacker IP address between 172.16.0.1 - 172.16.0.254
        2. Scan addresses 192.168.0.1 - 192.168.0.10
        3. Pick a random victim IP address between 192.168.0.1 - 192.168.0.10
        4. Wait 10 seconds
        5. Successful Telnet connection to the random victim address (3)

    :param event: Optional CEF event to work with. The CEF original state is kept protected.
    :return:
    """

    if event is None:
        event = Cef()

    attacker_address = random.ip('172.16.0.1', '172.16.0.254')
    fake_scan_addresses = list(generate.ip('192.168.0.1', '192.168.0.10'))
    fake_victim_address = random.ip('192.168.0.1', '192.168.0.10')

    print('Simulating fake IP scan . . .')
    with event:
        event.name = 'Fake IP Scan Simulation'
        event.sourceAddress = attacker_address

        with event:
            event.message = 'Fake Ping'
            while fake_scan_addresses:
                event.destinationAddress = fake_scan_addresses.pop()
                yield event

        sleep(seconds=10)

        print("Simulating fake successful Telnet connection . . .")
        with event:
            event.message = 'Fake Successful Telnet'
            event.destinationPort = 23
            event.destinationAddress = fake_victim_address
            yield event

    print("Done simulating.")
