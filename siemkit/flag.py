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


def is_on(flags, enum_flag):
    return (flags & enum_flag.value) == enum_flag.value


def set_on(flags, enum_flag):
    return flags | enum_flag.value


def set_off(flags, enum_flag):
    return flags & ~enum_flag.value


def toggle(flags, enum_flag):
    return flags ^ enum_flag.value


def get(flags, enum):
    for enum_flag in enum:
        yield enum_flag.name, is_on(flags, enum_flag)


def get_active(flags, enum):
    for enum_flag in enum:
        if get(flags, enum_flag):
            yield enum_flag.name
