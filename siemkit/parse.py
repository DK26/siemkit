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

import datetime

import pytimeparse
# * pytimeparse - MIT License
#     by: wroberts
#     source: https://github.com/wroberts/pytimeparse

import hfilesize
#  * hfilesize - MIT License
#     by: simonzack
#     source: https://github.com/simonzack/hfilesize

import dateparser
# * dateparser - BSD 3-Clause License
#     source: https://github.com/scrapinghub/dateparser
#     license: https://github.com/scrapinghub/dateparser/blob/master/LICENSE


def time(time_string: str) -> datetime.datetime:
    """
    Parse a time string into a datetime object.

        e.g.:

        A string of:
         "21/11/1988"

        Results in:
         datetime.datetime(1988, 11, 21, 0, 0)

    Relative time ("ago") is also supported:

        A string of:
         "1 day ago"

        Results in a `datetime` object set to 1 day before
         the current time of execution.


    :param time_string:
    :return: datetime object
    """
    return dateparser.parse(time_string)


def timedelta(time_delta_string: str) -> datetime.timedelta:
    """
    Parse a time delta string into a timedelta object

        e.g.:

        A string of:
         "2 weeks, 1 day, 12 hours, 30 minutes and 15 seconds"

        Results in:
         datetime.timedelta(days=15, seconds=45015)

    :param time_delta_string:
    :return: timedelta object
    """
    time_delta_string = time_delta_string.lower().replace("and", '').replace('every', '')
    return datetime.timedelta(seconds=pytimeparse.parse(time_delta_string))


def size(size_string: str) -> int:
    """
    Parse a file or bandwidth string unit size to a bytes size.

        e.g.:

        A string of:
            "10MB"

        Results in:
            10485760

    :param size_string:
    :return:
    """
    return hfilesize.FileSize(size_string)


def boolean(bool_string: str) -> bool:
    bool_string = bool_string.lower()
    return bool_string in ('t', 'true', 'yes', 'ok', 'on', '1', 'some')
