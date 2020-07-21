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

import os
import json
from typing import Generator
from typing import Tuple
from typing import Set
from typing import Dict
from typing import Collection
from collections.abc import Iterable
from siemkit.file import open


class IDTracker:

    def __init__(self, file_name):

        self.__file_name = file_name

        self.__data = {}

        self.__update = True

        if os.path.exists(self.__file_name):
            self.load()
        else:
            path = os.path.dirname(self.__file_name)
            if path:
                if not os.path.exists(path):
                    os.makedirs(path)
            self.save()

    def exist(self, key, item):
        result = self.__data.get(key)
        return result is not None and item in result

    def remember(self, key, value):
        if key in self.__data.keys():
            self.__data[key].add(value)
        else:
            self.__data[key] = {value}
        self.__update = True

    def save(self):
        if self.__update:
            with open(self.__file_name, 'wb') as fs:

                json.dump(self.__data, fs)
            self.__update = False

    def load(self):
        with open(self.__file_name, 'rb') as fs:
            self.__data = json.load(fs)

        self.__update = False

    def __contains__(self, item):
        key, value = item
        return self.exist(key, value)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            raise

        self.save()

    def __str__(self):
        return str(self.__data)


class JSONFile(dict):

    def __init__(self, file_name, *args, auto_commit=False, indent=4, **kwargs):

        self.__file_name = file_name
        self.__auto_commit = auto_commit
        self.__indent = indent

        if os.path.exists(file_name):
            self.load()

        # Assign other values.
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.__auto_commit:
            self.commit()

    def commit(self):
        with open(self.__file_name, 'w', encoding='utf-8', errors='ignore') as fs:
            json.dump(self, fs, indent=self.__indent)

    def load(self):
        with open(self.__file_name, 'r', encoding='utf-8', errors='ignore') as fs:
            self.clear()
            self.update(json.load(fs))
        return self


def test_id_tracker():

    import os

    user_id = 'User2'

    fake_data1 = {
        'stuff': [
            {'id': 123},
            {'id': 564},
            {'id': 111}
        ]
    }
    fake_data2 = {
        'stuff': [
            {'id': 121},
            {'id': 564},
            {'id': 111}
        ]
    }

    tracker_file = 'test.id.tracker'
    print(f"Tracker Exists?: {os.path.exists(tracker_file)}")

    data_tracker = IDTracker(tracker_file)

    for stuff in fake_data2['stuff']:
        if (user_id, stuff['id']) not in data_tracker:
            print(f"New stuff! {user_id}:{stuff['id']}")
            data_tracker.remember(user_id, stuff['id'])
        else:
            print(f"Stuff already there... {user_id}:{stuff['id']}")

    data_tracker.save()

    print(data_tracker)

    os.remove(tracker_file)


def get_multi_keys(dictionary, keys):

    values = []
    for key in keys:
        values.append(dictionary[key])

    return values


def map_multi_keys(dictionary, keys):
    return tuple(get_multi_keys(dictionary, keys)), dictionary


def multi_keys_dict(dict_collection, keys):
    for dict_item in dict_collection:
        k, v = map_multi_keys(dict_item, keys)
        yield {k: v}


def assure_tuple(value):
    if isinstance(value, str):
        value = (value,)
    else:
        value = tuple(value)
    return value


def swapped_dict(dictionary: dict) -> dict:
    """
    Created a new dictionary with swapped keys & values of a given dictionary argument.
    :param dictionary:
    :return:
    """
    return {v: k for k, v in dictionary.items()}


def swap_dict(dictionary: dict) -> Generator[Tuple[object, object], None, None]:
    """
    Iterate over a dictionary & generate swapped key, value tuple.
    :param dictionary:
    :return:
    """
    for k, v in dictionary.items():
        yield v, k


def extract_words(item, global_set: Set):
    """
    Deep scan for strings, returning a searchable set for unique values.
    :param item:
    :param global_set:
    :return:
    """

    if isinstance(item, dict):
        for k, v in item.items():
            extract_words(k, global_set)
            extract_words(v, global_set)
    elif isinstance(item, str):
        global_set.add(item)
    elif isinstance(item, Iterable):
        for i in item:
            extract_words(i, global_set)


def words_set(item) -> Set:

    options = set()

    extract_words(item, options)

    return options


def key_map(data_: Collection) -> dict:
    """
    Map all keys in a given data collection to their respective values.

    e.g.

    For the next data collection:

        data = [
            {
                'name': 'foo',
                'age': 31,
                'country': 'UK'
            },
            {
                'name': 'bar',
                'age': 31,
                'country': 'US'
            },
            {
                'name': 'Mr. X',
                'age': 29,
                'country': 'UK'
            }
        ]

    mapped_data = key_mep(data)

    mapped_data['age'][31]
        will return:
            [
                {
                    'name': 'foo',
                    'age': 31,
                    'country': 'UK'
                },
                {
                    'name': 'bar',
                    'age': 31,
                    'country': 'US'
                }
            ]

    mapped_data['country']['UK']
        will return:
            [
                {
                    'name': 'foo',
                    'age': 31,
                    'country': 'UK'
                },
                {
                    'name': 'Mr. X',
                    'age': 29,
                    'country': 'UK'
                }
            ]

    :param data_:
    :return:
    """

    mapped_data = {}

    for item in data_:
        for k, v in item.items():
            if k not in mapped_data:
                mapped_data[k] = {}
            if v not in mapped_data[k]:
                mapped_data[k][v] = []
            mapped_data[k][v].append(item)

    return mapped_data


if __name__ == '__main__':
    test_id_tracker()
