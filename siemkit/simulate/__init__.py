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

from siemkit.event import Cef
from random import randint
# ToDo: Correlation Event
# ToDo: Random Number Event


def random_number(start_range=0, end_range=4, amount=1, event=None):

    if event is None:
        event = Cef()

    for _ in range(amount):
        event.deviceCustomNumber1 = randint(start_range, end_range)
        yield event

