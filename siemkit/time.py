#   Copyright © 2020 CyberSIEM ®
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

from datetime import datetime
from datetime import timedelta
from math import floor


def ago(*args, **kwargs) -> datetime:
    """
    Calculates a timedelta from now.

    e.g.
        ago(days=3)
        ago(days=3 * 365)  # 3 Years ago

    All arguments are passed to the underlying timedelta() object.
        ago(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    :return datetime
    """
    return datetime.now() - timedelta(*args, **kwargs)


def timestamp(datetime_: datetime, utc=False) -> int:
    """
    Turns a datetime into a Java Timestamp (Milliseconds Epoch).

    :param datetime_: datetime object
    :param utc: When True, will change the `datetime_` object to its relative UTC time.
    :return: Milliseconds Epoch Timestamp
    """
    ts = datetime_.timestamp()

    if utc:
        ts = (datetime.utcfromtimestamp(ts).timestamp())

    return floor(ts * 1000)
