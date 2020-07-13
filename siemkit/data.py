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

import os
import pickle


# ToDo: Replace pickle with JSON dump. REF: https://pycharm-security.readthedocs.io/en/latest/checks/PIC100.html
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

                pickle.dump(self.__data, fs)
            self.__update = False

    def load(self):
        with open(self.__file_name, 'rb') as fs:
            self.__data = pickle.load(fs)

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


if __name__ == '__main__':
    test_id_tracker()
