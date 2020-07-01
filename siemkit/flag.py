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

from enum import Enum
from enum import EnumMeta
from typing import Generator
from typing import Tuple


def is_on(flags: int, enum_flag: Enum) -> bool:
    return (flags & enum_flag.value) == enum_flag.value


def set_on(flags: int, enum_flag: Enum) -> int:
    return flags | enum_flag.value


def set_off(flags: int, enum_flag: Enum) -> int:
    return flags & ~enum_flag.value


def toggle(flags: int, enum_flag: Enum) -> int:
    return flags ^ enum_flag.value


def get(flags: int, enum: EnumMeta) -> Generator[Tuple[Enum, bool], None, None]:
    """
    Yields given `flags` integer as Enums with their boolean status.
    :param flags:
    :param enum:
    :return:
    """
    for enum_flag in enum:
        yield enum_flag, is_on(flags, enum_flag)


def get_active(flags: int, enum: EnumMeta) -> Generator[Enum, None, None]:
    """
    Yields active Enum flags from the given `flags` integer parameter.
    :param flags:
    :param enum:
    :return:
    """
    for enum_flag in enum:
        if is_on(flags, enum_flag):
            yield enum_flag
