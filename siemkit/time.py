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
from datetime import timezone
from datetime import tzinfo
from math import floor
import time


def sleep(*args, **kwargs):
    """
    Calculates timedelta for sleeping

    e.g.
        sleep(days=3)
        sleep(days=365 * 3)  #  Sleep 3 years

        All arguments are passed to the underlying timedelta() object.
            sleep(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    """
    time.sleep(timedelta(*args, **kwargs).total_seconds())


def millis(*args, **kwargs) -> int:
    """
    Calculates timedelta to milliseconds

    e.g.
        millis(days=3)
        millis(days=365 * 3)  # 3 Years in milliseconds

        All arguments are passed to the underlying timedelta() object.
            millis(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    :return milliseconds
    """
    return floor(timedelta(*args, **kwargs).total_seconds() * 1000)


def ago(*args, **kwargs) -> datetime:
    """
    Calculates a timedelta from now.

    e.g.
        ago(days=3)
        ago(days=365 * 3)  # 3 Years ago

    All arguments are passed to the underlying timedelta() object.
        ago(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    :return A 'datetime' object.
    """
    return datetime.now() - timedelta(*args, **kwargs)


def to_timestamp(datetime_: datetime, utc=False) -> int:
    """
    Turns a datetime into a Milliseconds Epoch Timestamp ("Java Timestamp").

    :param datetime_: datetime object
    :param utc: When True, will change the `datetime_` object to its relative UTC time.
    :return: Milliseconds Epoch Timestamp
    """
    ts = datetime_.timestamp()

    if utc:
        ts = (datetime.utcfromtimestamp(ts).timestamp())

    return floor(ts * 1000)


def from_timestamp(timestamp, utc=False) -> datetime:
    """
    Create a datetime out of a Milliseconds Epoch Timestamp ("Java Timestamp").
    :param timestamp:
    :param utc: If True, this will return a 'datetime' object that is self-aware of its UTC timezone status.
                This will keep its behaviour consistent when interacting with its methods.
    :return: A 'datetime' object.
    """
    ts = floor(int(timestamp) / 1000)

    if utc:
        return datetime.fromtimestamp(ts, timezone.utc)

    return datetime.fromtimestamp(ts)


def to_format(datetime_: datetime, format_="%b %d %Y %H:%M:%S") -> str:
    """
    Convert datetime to a default format.
    :param datetime_:
    :param format_:
    :return:
    """
    return datetime_.strftime(format_)


def utc_to_tz(datetime_: datetime, tz: tzinfo = None) -> datetime:
    """
    Convert a UTC datetime object to another time zone.
        by default will convert to local time zone.
    :param datetime_:
    :param tz:
    :return:
    """
    return datetime_.replace(tzinfo=timezone.utc).astimezone(tz=tz)
