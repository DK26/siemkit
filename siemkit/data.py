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
        return result and item in result

    def remember(self, key, value):
        if key in self.__data:
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
