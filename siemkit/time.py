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
from abc import ABC
from abc import abstractmethod
from inspect import isclass
import time

UTC = timezone.utc


class Timestamp(ABC):
    """
    An interface for implementing a proper Timestamp.
        Once you implement it, make sure you also define it in the `TimeType` enum class.
    """

    @classmethod
    @abstractmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:
        """
        A static method to convert a datetime into a timestamp of this time type.
        :param datetime_:
        :param tz: Timezone to convert to. Default is None.
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:
        """
        A static method to convert a timestamp of this time type into a datetime.
        :param timestamp:
        :param tz: Timezone of the the timestamp to let the datetime know its timezone.
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def delta(cls, *args, **kwargs) -> int:
        """
        A static method to convert time delta arguments into time units of this time type.

        e.g.
            delta(days=3)
            delta(days=365 * 3)  # 3 Years in milliseconds (default TimeType: time.TimeType.EPOCH_MILLIS).

            delta(days=3, type_=time.TimeType.EPOCH)  # 3 days in seconds (time.TimeType.EPOCH).

            All arguments are passed to the underlying timedelta() object.
                delta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

        :param args:
        :param kwargs:
        :return:
        """
        pass


class EpochTimestamp(Timestamp):

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:
        return floor(datetime_.astimezone(tz=tz).timestamp())

    @classmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:
        return datetime.fromtimestamp(timestamp).replace(tzinfo=tz)

    @classmethod
    def delta(cls, *args, **kwargs) -> int:
        return floor(timedelta(*args, **kwargs).total_seconds())


class EpochMillisTimestamp(Timestamp):

    PRECISION = 1_000

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:
        return floor(datetime_.astimezone(tz=tz).timestamp() * cls.PRECISION)

    @classmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:
        return datetime.fromtimestamp(int(timestamp) / cls.PRECISION).replace(tzinfo=tz)

    @classmethod
    def delta(cls, *args, **kwargs) -> int:
        return floor(timedelta(*args, **kwargs).total_seconds() * cls.PRECISION)


class LDAPTimestamp(Timestamp):
    """
    Converts a Microsoft Win32 FILETIME timestamp (aka LDAP / Active Directory timestamp)
     into & from a datetime object.
    """

    LDAP_START_TIME = datetime(1601, 1, 1)

    EPOCH_START_TIME = 116_444_736_000_000_000

    PRECISION = 10_000_000

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:

        datetime_ = datetime_.astimezone(tz=tz)

        ldap_timestamp = (datetime_.timestamp() * cls.PRECISION) + cls.EPOCH_START_TIME

        return floor(ldap_timestamp)

    @classmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:

        epoch_datetime = cls.LDAP_START_TIME + timedelta(
            seconds=(timestamp / cls.PRECISION)
        )

        epoch_datetime = epoch_datetime.replace(tzinfo=UTC).astimezone(tz=None)

        return epoch_datetime.replace(tzinfo=tz)

    @classmethod
    def delta(cls, *args, **kwargs) -> int:
        return floor(timedelta(*args, **kwargs).total_seconds() * cls.PRECISION)


class TimeType(Enum):

    EPOCH = EpochTimestamp
    EPOCH_MILLIS = EpochMillisTimestamp
    LDAP = LDAPTimestamp


default = {
    'format': "%b %d %Y %H:%M:%S",
    'tz': None,
    'type': TimeType.EPOCH_MILLIS
}


def time_type(time_type_enum: TimeType) -> Timestamp:
    """
    Return reference to a Timestamp class of a given TimeType enum argument or the default Timestamp.
    :param time_type_enum:
    :return: Timestamp Class reference
    """

    if time_type_enum is None or not (isclass(time_type_enum.value)
                                      and issubclass(time_type_enum.value, Timestamp)):
        time_type_class = default.get('type', TimeType.EPOCH_MILLIS).value
    else:
        time_type_class = time_type_enum.value

    return time_type_class


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


def ago(type_: TimeType = None, *args, **kwargs) -> int:
    """
    Calculates the date & time from now, in time delta parameters.

    e.g.
        ago(days=3)
        ago(days=365 * 3)  # 3 Years ago in milliseconds (default TimeType: time.TimeType.EPOCH_MILLIS).

        ago(days=3, type_=time.TimeType.EPOCH)  # 3 days ago in seconds (time.TimeType.EPOCH).

    All arguments are passed to the underlying timedelta() object.
        ago(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    :return A 'datetime' object.
    """
    return time_type(type_).from_datetime(datetime.now() - timedelta(*args, **kwargs))


def delta(type_: TimeType = None, *args, **kwargs) -> int:
    return time_type(type_).delta(*args, **kwargs)


def to_timestamp(datetime_: datetime, tz=None, type_: TimeType = None) -> int:
    return time_type(type_).from_datetime(datetime_, tz)


def from_timestamp(timestamp: int, tz=None, type_: TimeType = None) -> datetime:
    return time_type(type_).to_datetime(timestamp, tz)


def to_format(datetime_: datetime, format_: str = None) -> str:
    """
    Convert a datetime object to a default or given time format.
     A default time format can be assigned globally to `siemkit.time.default['format']`.

    :param datetime_:
    :param format_:
    :return:
    """
    if not format_:
        format_ = default.get("format", "%b %d %Y %H:%M:%S")

    return datetime_.strftime(format_)


def from_format(date_string: str, format_: str = None) -> datetime:
    """
    Format a time string with a default or given time format into a datetime object.
     A default time format can be assigned globally to `siemkit.time.default['format']`.

    :param date_string:
    :param format_:
    :return:
    """
    if not format_:
        format_ = default.get("format", "%b %d %Y %H:%M:%S")

    return datetime.strptime(date_string, format_)


def utc_to_tz(datetime_: datetime, tz: tzinfo = None) -> datetime:
    """
    Converts a UTC datetime object to a different time zone.
        by default will convert to the system's local time zone.

     A default time zone can be assigned globally to `siemkit.time.default['tz']`.

    :param datetime_:
    :param tz:
    :return:
    """
    if not tz:
        tz = default.get("tz")

    return datetime_.replace(tzinfo=timezone.utc).astimezone(tz=tz)
