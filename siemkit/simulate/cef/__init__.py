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
# ToDo: Correlation Event
# ToDo: Random Number Event


def random_number(start_range=None, end_range=None, amount=1, event=None) -> Generator[Cef, None, None]:

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


def fake_ip_scan(event=None):
    """
    Simulate a fake IP scan & telnet login.
    :param amount:
    :param time_gap:
    :param event:
    :return:
    """

    if event is None:
        event = Cef()

    attacker_address = random.ip('172.16.0.1', '172.16.0.254')
    fake_scan_addresses = list(generate.ip('192.168.0.1', '192.168.0.254'))
    fake_victim_address = random.ip('192.168.0.1', '192.168.0.254')

    print('Simulating fake IP scan . . .')
    with event:
        event.name = 'Fake IP Scan Simulation'
        event.sourceAddress = attacker_address

        with event:
            event.message = 'Ping'
            while fake_scan_addresses:
                with event:
                    event.destinationAddress = fake_scan_addresses.pop()
                    yield event

        sleep(seconds=10)

        print("Simulating a fake successful Telnet connection . . .")
        with event:
            event.message = 'Fake Successful Telnet'
            event.destinationPort = 23
            event.destinationAddress = fake_victim_address
            yield event

        print("Done simulating.")
