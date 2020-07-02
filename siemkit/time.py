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

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from datetime import tzinfo
from math import floor
from enum import Enum
import time


DEFAULT = {
    'format': "%b %d %Y %H:%M:%S",
    'tz': None
}


class Timestamp:
    @classmethod
    def from_datetime(cls, datetime_):
        pass

    @classmethod
    def to_datetime(cls, timestamp):
        pass


class EpochTimestamp(Timestamp):
    @classmethod
    def from_datetime(cls, datetime_):
        pass

    @classmethod
    def to_datetime(cls, timestamp):
        pass


class EpochMillisTimestamp(Timestamp):
    @classmethod
    def from_datetime(cls, datetime_):
        pass

    @classmethod
    def to_datetime(cls, timestamp):
        pass


class LDAPTimestamp(Timestamp):
    @classmethod
    def from_datetime(cls, datetime_):
        pass

    @classmethod
    def to_datetime(cls, timestamp):
        pass


class TimestampType(Enum):

    EPOCH = EpochTimestamp
    EPOCH_MILLIS = EpochMillisTimestamp
    LDAP = LDAPTimestamp


def sleep(*args, **kwargs):
    """
    Sleeps a given time delta parameters.

    e.g.
        sleep(days=3)
        sleep(days=365 * 3)  #  Sleep 3 years

        All arguments are passed to the underlying timedelta() object.
            sleep(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    """
    time.sleep(timedelta(*args, **kwargs).total_seconds())


def to_millis(datetime_: datetime, tz=None) -> int:

    return floor(utc_to_tz(datetime_, tz).timestamp() * 1000)


def millis(*args, **kwargs) -> int:
    """
    Converts time delta parameters to milliseconds.

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
    Calculates the date & time from now, in time delta parameters.

    e.g.
        ago(days=3)
        ago(days=365 * 3)  # 3 Years ago

    All arguments are passed to the underlying timedelta() object.
        ago(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    :return A 'datetime' object.
    """
    return datetime.now() - timedelta(*args, **kwargs)


def to_timestamp(datetime_: datetime, utc: bool = False) -> int:
    """
    Turns a datetime object into a milliseconds epoch timestamp ("Java Timestamp").

    :param datetime_: datetime object
    :param utc: If True, converts the local time zone datetime object to a UTC timestamp.
    :return: Milliseconds Epoch Timestamp
    """
    ts = datetime_.timestamp()

    if utc:
        ts = (datetime.utcfromtimestamp(ts).timestamp())

    return floor(ts * 1000)


def from_timestamp(timestamp: 'int or str of milliseconds', localize: bool = False, tz: tzinfo = None) -> datetime:
    """
    Create a datetime object out of a milliseconds epoch timestamp ("Java Timestamp").

     A default time zone can be assigned globally to `siemkit.time.DEFAULT['tz']`.

    :param timestamp: Milliseconds epoch timestamp.
    :param localize: If True, converts UTC timestamp to a localized datetime.
    :param tz: Timezone for the UTC timestamp localization.
                By default uses the local system time zone (None).
    :return: A 'datetime' object.
    """
    ts = int(timestamp) / 1000

    if localize:
        if not tz:
            tz = DEFAULT.get("tz")
        return utc_to_tz(datetime.fromtimestamp(ts), tz=tz)

    return datetime.fromtimestamp(ts)


def to_format(datetime_: datetime, format_: str = None) -> str:
    """
    Convert a datetime object to a default or given time format.
     A default time format can be assigned globally to `siemkit.time.DEFAULT['format']`.

    :param datetime_:
    :param format_:
    :return:
    """
    if not format_:
        format_ = DEFAULT.get("format", "%b %d %Y %H:%M:%S")

    return datetime_.strftime(format_)


def from_format(date_string: str, format_: str = None) -> datetime:
    """
    Format a time string with a default or given time format into a datetime object.
     A default time format can be assigned globally to `siemkit.time.DEFAULT['format']`.

    :param date_string:
    :param format_:
    :return:
    """
    if not format_:
        format_ = DEFAULT.get("format", "%b %d %Y %H:%M:%S")

    return datetime.strptime(date_string, format_)


def utc_to_tz(datetime_: datetime, tz: tzinfo = None) -> datetime:
    """
    Converts a UTC datetime object to a different time zone.
        by default will convert to the system's local time zone.

     A default time zone can be assigned globally to `siemkit.time.DEFAULT['tz']`.

    :param datetime_:
    :param tz:
    :return:
    """
    if not tz:
        tz = DEFAULT.get("tz")

    return datetime_.replace(tzinfo=timezone.utc).astimezone(tz=tz)


def from_filetime(timestamp: int) -> datetime:
    """
    Converts a Microsoft Win32 FILETIME timestamp (aka LDAP / Active Directory timestamp)
     into a datetime object.

    :param timestamp: Microsoft Win32 FILETIME timestamp
    :return:
    """
    filetime_start_time = datetime(1601, 1, 1)
    extra_nanoseconds_precision = 10_000_000

    epoch_datetime = filetime_start_time + timedelta(
        seconds=(timestamp / extra_nanoseconds_precision)
    )

    return epoch_datetime


def to_filetime(datetime_: datetime) -> int:
    """
    Converts a datetime object into
     a Microsoft Win32 FILETIME timestamp (aka LDAP / Active Directory timestamp)

    :param datetime_:
    :return: Microsoft Win32 FILETIME timestamp
    """
    datetime_ = utc_to_tz(datetime_, tz=None)  # Replace default UTC timezone to local (None).

    epoch_start_time = 116_444_736_000_000_000
    extra_nanoseconds_precision = 10_000_000

    filetime = (datetime_.timestamp() * extra_nanoseconds_precision) + epoch_start_time

    return int(filetime)

