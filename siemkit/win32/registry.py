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

import winreg
from enum import IntEnum
from typing import Tuple
from collections import deque


class HKEY(IntEnum):

    CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
    CURRENT_USER = winreg.HKEY_CURRENT_USER
    LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
    USERS = winreg.HKEY_USERS
    CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG


hkey_dictionary = {
    'HKEY_CLASSES_ROOT': HKEY.CLASSES_ROOT,
    'HKEY_CURRENT_USER': HKEY.CURRENT_USER,
    'HKEY_LOCAL_MACHINE': HKEY.LOCAL_MACHINE,
    'USERS': HKEY.USERS,
    'CURRENT_CONFIG': HKEY.CURRENT_CONFIG
}


def get_key_parse(path: str) -> Tuple[str, int]:

    root = ''

    path_parts = path.split('\\')
    path_parts_deque = deque(path_parts)

    key = path_parts_deque.pop()

    for part in path_parts:
        upper_part = part.upper()
        if upper_part.startswith('HKEY_'):
            root = upper_part
            path_parts_deque.popleft()
            break
        else:
            path_parts_deque.popleft()

    return get_key(hkey_dictionary[root], '\\'.join(path_parts_deque), key)


def set_key_parse(path: str, value, key_type=winreg.REG_EXPAND_SZ):
    root = ''

    path_parts = path.split('\\')
    path_parts_deque = deque(path_parts)

    key = path_parts_deque.pop()

    for part in path_parts:
        upper_part = part.upper()
        if upper_part.startswith('HKEY_'):
            root = upper_part
            path_parts_deque.popleft()
            break
        else:
            path_parts_deque.popleft()

    set_key(hkey_dictionary[root], '\\'.join(path_parts_deque), key, value, key_type)


def get_key(root: int, path: str, key: str) -> Tuple[str, int]:

    # REF: https://stackoverflow.com/questions/15128225/python-script-to-read-and-write-a-path-to-registry

    value = None
    type_ = None

    with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as registry_key:
        value, type_ = winreg.QueryValueEx(registry_key, key)

    return value, type_


def set_key(root: int, path: str, key: str, value: str, key_type=winreg.REG_EXPAND_SZ):

    # REF: https://stackoverflow.com/questions/15128225/python-script-to-read-and-write-a-path-to-registry

    winreg.CreateKey(root, path)
    with winreg.OpenKey(root, path, 0, winreg.KEY_WRITE) as registry_key:
        winreg.SetValueEx(registry_key, key, 0, key_type, value)
