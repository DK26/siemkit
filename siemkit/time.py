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

# ToDo: 1. Timeformats -> Have the time.py to either specify a format to parse, turn into a timestamp,
#  or have the 'auto' string for using the timeparse library.
# ToDo: 2. Add a string enum for known & common timeformats.

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from datetime import tzinfo
from math import floor
from enum import Enum
from abc import ABC
from abc import abstractmethod
from inspect import isclass
from typing import Union
import time

UTC = timezone.utc


def pick_timedelta(timedelta_, *args, **kwargs) -> timedelta:
    """
    Picks between a given timedelta object or timedelta arguments such as: days, minutes, etc.
        If a timedelta object is passed as an argument, the rest of the arguments will be ignored.

    :param timedelta_: timedelta object
    :param args & kwargs: days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
    :return: The timedelta object to be passed to the caller.
    """
    if isinstance(timedelta_, timedelta):
        given_timedelta = timedelta_
    else:
        given_timedelta = timedelta(*args, **kwargs)
    return given_timedelta


class Timestamp(ABC):
    """
    An interface for implementing a proper Timestamp.
        Once you implement it, make sure you also define it in the `TimeType` enum class.
    """

    PRECISION = 1

    @classmethod
    @abstractmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> Union[int, str]:
        """
        A static method to convert a datetime into a timestamp of this time type.
        :param datetime_:
        :param tz: Timezone to convert to. Default is None.
        :return:
        """
        raise NotImplementedError("'from_datetime()' method must be implemented.")

    @classmethod
    @abstractmethod
    def to_datetime(cls, timestamp: Union[int, str], tz: tzinfo = None) -> datetime:
        """
        A static method to convert a timestamp of this time type into a datetime.
        :param timestamp:
        :param tz: Timezone of the the timestamp to let the datetime know its timezone.
        :return:
        """
        raise NotImplementedError("'to_datetime()' method must be implemented.")

    @classmethod
    def delta(cls, timedelta_: timedelta = None, *args, **kwargs) -> int:
        """
        A static method to convert time delta arguments into time units of this time type.

        e.g.
            delta(days=3)
            delta(days=365 * 3)  # 3 Years in milliseconds (default TimeType: time.TimeType.EPOCH_MILLIS).

            delta(days=3, type_=time.TimeType.EPOCH)  # 3 days in seconds (time.TimeType.EPOCH).

            All arguments are passed to the underlying timedelta() object.
                delta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

        :param timedelta_: A timedelta object. Overrides any other time delta parameters.
        :param args:
        :param kwargs:
        :return:
        """
        return floor(pick_timedelta(timedelta_, *args, **kwargs).total_seconds() * cls.PRECISION)


class EpochTimestamp(Timestamp):

    PRECISION = 1

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:
        return floor(datetime_.astimezone(tz=tz).timestamp())

    @classmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:
        return datetime.fromtimestamp(timestamp).replace(tzinfo=tz)


class EpochMillisTimestamp(Timestamp):

    PRECISION = 1_000

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:
        return floor(datetime_.astimezone(tz=tz).timestamp() * cls.PRECISION)

    @classmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:
        return datetime.fromtimestamp(int(timestamp) / cls.PRECISION).replace(tzinfo=tz)


class FiletimeTimestamp(Timestamp):
    """
    Converts a Microsoft Win32 FILETIME timestamp (aka LDAP / Active Directory timestamp)
     into & from a datetime object.
    """

    FILETIME_START_TIME = datetime(1601, 1, 1)

    EPOCH_START_TIME = 116_444_736_000_000_000

    PRECISION = 10_000_000

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> int:

        datetime_ = datetime_.astimezone(tz=tz)

        ldap_timestamp = (datetime_.timestamp() * cls.PRECISION) + cls.EPOCH_START_TIME

        return floor(ldap_timestamp)

    @classmethod
    def to_datetime(cls, timestamp: int, tz: tzinfo = None) -> datetime:

        epoch_datetime = cls.FILETIME_START_TIME + timedelta(
            seconds=(timestamp / cls.PRECISION)
        )

        epoch_datetime = epoch_datetime.replace(tzinfo=UTC).astimezone(tz=None)

        return epoch_datetime.replace(tzinfo=tz)


class LdapTimestamp(Timestamp):

    @classmethod
    def from_datetime(cls, datetime_: datetime, tz: tzinfo = None) -> str:

        zulu_time_zone = '.0Z'

        return (
            datetime_
                .replace(tzinfo=tz)
                .astimezone(tz=timezone.utc)
                .strftime("%Y%m%d%H%M%S") + zulu_time_zone
        )

    @classmethod
    def to_datetime(cls, timestamp: str, tz: tzinfo = None) -> datetime:

        zulu_time_zone = '.0Z'

        return (
            datetime
                .strptime(timestamp, "%Y%m%d%H%M%S" + zulu_time_zone)
                .replace(tzinfo=timezone.utc)
                .astimezone(tz=tz)
        )


class TimeType(Enum):

    EPOCH = EpochTimestamp
    EPOCH_MILLIS = EpochMillisTimestamp
    FILETIME = FiletimeTimestamp
    LDAP = LdapTimestamp


default = {
    'format': "%b %d %Y %H:%M:%S",
    'tz': None,
    'type': TimeType.EPOCH_MILLIS
}


def time_type(time_type_enum: TimeType) -> Timestamp:
    """
    Returns a reference to a Timestamp object of a given TimeType enum argument
     or the default Timestamp object.

    :param time_type_enum:
    :return: Timestamp reference
    """
    if isinstance(time_type_enum, Timestamp):
        return time_type_enum

    if time_type_enum is None or not (isclass(time_type_enum.value)
                                      and issubclass(time_type_enum.value, Timestamp)):
        time_type_class = default.get('type', TimeType.EPOCH_MILLIS).value
    else:
        time_type_class = time_type_enum.value

    return time_type_class


def sleep(timedelta_: timedelta = None, *args, **kwargs):
    """
    Sleeps a given time delta parameters or a timedelta object period.

    e.g.
        sleep(days=3)
        sleep(days=365 * 3)  #  Sleep 3 years

        All arguments are passed to the underlying timedelta() object.
            sleep(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

        action_wait_period = timedelta(days=1, hours=12)
        sleep(action_wait_period)
    or
        sleep(timedelta_=action_wait_period)

    """
    time.sleep(pick_timedelta(timedelta_, *args, **kwargs).total_seconds())


def ago(timedelta_: timedelta = None, type_: TimeType = None, *args, **kwargs) -> int:
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

    return time_type(type_).from_datetime(datetime.now() - pick_timedelta(timedelta_, *args, **kwargs))


def delta(timedelta_: timedelta = None, type_: TimeType = None, *args, **kwargs) -> int:
    return time_type(type_).delta(timedelta_, *args, **kwargs)


def to_timestamp(datetime_: datetime, tz=None, type_: TimeType = None) -> int:
    return time_type(type_).from_datetime(datetime_, tz)


def from_timestamp(timestamp: int, tz=None, type_: TimeType = None) -> datetime:
    return time_type(type_).to_datetime(timestamp, tz)


def to_format(datetime_: datetime = None, format_: str = None, tz: tzinfo = None) -> str:
    """
    Convert a datetime object to a default or given time format.
     A default time format can be assigned globally to `siemkit.time.default['format']`.

    :param datetime_:
    :param format_:
    :param tz:
    :return:
    """
    if datetime_ is None:
        datetime_ = datetime.now()

    if not format_:
        format_ = default.get("format", "%b %d %Y %H:%M:%S")

    if not tz:
        tz = default.get("tz")

    return (datetime_
            .astimezone(tz=tz)
            .strftime(format_))


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


def current_timestamp(type_: TimeType = None, tz: tzinfo = None) -> int:
    """
    Create a current timestamp.
    :param type_: Timestamp type (default: time.TimeType.EPOCH_MILLIS)
    :param tz: Optional timezone. For UTC use `datetime.timezone.utc`.
    :return: Timestamp
    """
    return time_type(type_).from_datetime(datetime.now().astimezone(tz=tz))

