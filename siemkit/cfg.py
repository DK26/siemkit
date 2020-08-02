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

import csv
import shutil
import json
import os
from . import adaptors
from . import data

from typing import Tuple


class YamlManager(dict):

    # ToDo: Assign secrets fields to put in a Vault

    def __init__(
            self,
            yaml_adaptor: adaptors.Yaml,
            file_path: str,
            auto_commit: bool = False,
            root_manager: 'YamlManager' = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__yaml_adaptor = yaml_adaptor
        self.__file = file_path
        self.__auto_commit = auto_commit

        if root_manager is None:
            self.__root_manager = self
            self.reload()
        else:
            self.__root_manager = root_manager

    def __setitem__(self, key, value):

        super().__setitem__(key, value)

        if self.__auto_commit:
            self.__root_manager.commit()

        self.ready = True

    def __delitem__(self, key):

        super().__delitem__(key)

        if self.__auto_commit:
            self.__root_manager.commit()

    def commit(self):

        def reverse(d):

            if isinstance(d, YamlManager):

                result = {}
                for k, v in d.items():
                    if isinstance(v, YamlManager):
                        result[k] = reverse(v)
                    else:
                        result[k] = v

                return result
            else:
                return d

        with open(self.__file, 'w', encoding='utf-8', errors='ignore') as fs_:
            self.__yaml_adaptor.dump(reverse(self), fs_)

        return self

    def reload(self):

        def convert(d):

            if isinstance(d, dict):

                result = {}
                for k, v in d.items():
                    if isinstance(v, dict):
                        result[k] = convert(v)
                    else:
                        result[k] = v

                return YamlManager(self.__yaml_adaptor, self.__file, self.__auto_commit, self.__root_manager, result)
            else:
                return d

        if os.path.exists(self.__file):
            with open(self.__file, 'r', encoding='utf-8', errors='ignore') as fs_:
                self.clear()
                yaml_data = convert(self.__yaml_adaptor.load(fs_))
                if isinstance(yaml_data, dict):
                    self.update(yaml_data)

        return self


class CsvManager:

    # ToDo: Refactor to use a Vault

    def __init__(
            self,
            csv_file,
            key_fields,
            secret_fields=None,
            newline='',
            encoding='utf-8',
            errors='ignore',
            store_secret=None,
            get_secret=None,
            default_values=None
    ):
        """

        :param csv_file: A path to the configurations CSV file
        :param key_fields: An indexed field to group data by. e.g. username, id, email, etc.
        :param secret_fields: A collection of string field names to store their values in a vault.
        :param newline: Passed to the underlying FileStream handler of the CSV
        :param encoding: Passed to the underlying FileStream handler of the CSV
        :param errors: Passed to the underlying FileStream handler of the CSV

        :param store_secret: A store_secret() function/handler for storing secret fields.
                Parameters:
                    service - A static name for the App
                    username - A key under the service
                    password - A secret data
                Returns:
                    True if successful -> This is mandatory or else be treated as failure.

        :param get_secret: A get_secret() function/handler for restoring secret fields.
                Parameters:
                    service - A static name for the App
                    username - A key under the service
                Returns:
                    An exposed secret value as a UTF-8 string.

        :param default_values: A dictionary of default values in case if empty values.
        """

        key_fields = data.assure_tuple(key_fields)

        if secret_fields is None:
            secret_fields = set()

        for field in key_fields:
            if field in secret_fields:
                raise Exception(f"Secret field '{field}' cannot be part of a key field.")

        self._csv_file = csv_file
        self._key_fields = key_fields
        self._secret_fields = secret_fields
        self._newline = newline
        self._encoding = encoding
        self._errors = errors
        self._store_secret = store_secret
        self._get_secret = get_secret
        if default_values is None:
            default_values = {}
        self._default_values = default_values

        self._entries = None
        self._indexed_field_map = {}
        self._titles = None
        self._update = False

        self.load()

    def get_titles(self):
        return self._titles

    def get_entry(self, index):
        """
        Retrieves an entry by an index key from indexed data.

        Indexed data is predefined and mapped by the indexed field.
            e.g. username, id, email, ip_address, etc.

        csv_cfg = CSVConf(..,indexed_field='username',..)
        entry = csv_cfg.get_entry('<A username>')

        CSVConf(..,indexed_field='id',..)
        entry = csv_get.get_entry('<An ID number>')

        :param index: A key index to access the indexed field.
        :return: Entry dictionary
        """
        index = data.assure_tuple(index)

        return self._indexed_field_map[index]

    def set_entry(self, index, dict_values):
        index = data.assure_tuple(index)
        self._indexed_field_map[index] = dict_values

    def update_entry(self, index, dict_values):
        index = data.assure_tuple(index)
        self._indexed_field_map[index].update(dict_values)

    def exposed_entries(self):
        """
        Generates an exposed entry at a time, restoring its secret fields.
        :return:
        """

        for entry in self._entries:
            exposed_entry = dict(entry)

            for secret_field in self._secret_fields:
                exposed_entry[secret_field] = self.get_secret(self.construct_key(entry), secret_field)

            yield exposed_entry

    def get_entries(self) -> Tuple[dict]:
        return self._entries  # Already a tuple

    def construct_key(self, entry):
        new_key = []
        for key in self._key_fields:
            new_key.append(entry[key])

        return tuple(new_key)

    def store_secret(self, entry, secret_key):

        if callable(self._store_secret):
            key = f"{'.'.join(self.construct_key(entry))}.{secret_key}"

            if self._store_secret(key, entry[secret_key]):
                entry[secret_key] = 'stored'

        return self

    def get_secret(self, entry_index, secret_key):
        if callable(self._get_secret):
            """if isinstance(entry_index, str):
                entry_index = (entry_index,)
            else:
                entry_index = tuple(entry_index)
            """
            entry_index = data.assure_tuple(entry_index)
            key = f"{'.'.join(entry_index)}.{secret_key}"

            return self._get_secret(key)

    def get_key_fields(self):
        return self._key_fields

    def get_secret_fields(self):
        return self._secret_fields

    def save(self):
        """
        Commit changes to CSV file.
        :return: self
        """

        csv_file = self._csv_file
        csv_tmp_file = self._csv_file + '.tmp'

        with open(csv_tmp_file, 'w', encoding=self._encoding, errors=self._errors, newline=self._newline) as fs:
            fs.seek(0)
            writer = csv.DictWriter(fs, fieldnames=self._titles)
            writer.writeheader()
            for entry in self._entries:
                del entry['_line']
                writer.writerow(entry)

        # If we reach this point, then no exception occurred.
        # Otherwise, we are left a '.tmp' file to debug.
        shutil.move(csv_tmp_file, csv_file)

        return self

    def json_string(self, key=None, indent=4):

        json_copy = {}
        for k, v in self._indexed_field_map.items():
            json_copy['.'.join(k)] = v

        if key is None:
            return json.dumps(json_copy, indent=indent)
        else:
            key = data.assure_tuple(key)

        return json.dumps(json_copy['.'.join(key)], indent=indent)

    def load(self):
        """
        Load or Reload CSV file.
        :return: self
        """

        update = [False]

        def load_entries(update_):

            with open(self._csv_file, 'r', newline=self._newline, encoding=self._encoding, errors=self._errors) as fs:

                self._titles = tuple(next(csv.reader(fs)))

                fs.seek(0)

                csv_dict_ = csv.DictReader(fs)

                for i, row in enumerate(csv_dict_):

                    dict_row = dict(row)
                    dict_row['_line'] = i + 1

                    for k in dict_row.keys():

                        # Check secret field
                        if k in self._secret_fields:
                            if str(dict_row[k]).lower().strip() != 'stored':
                                if callable(self._store_secret):
                                    self.store_secret(dict_row, k)

                                    # Mark for update.
                                    # The list approach is a hack to manage reference,
                                    #  as the generator is unable to reach the outer 'update' variable,
                                    #  not even with `global update`.
                                    update_[0] = True

                        # Check default value for field
                        elif k in self._default_values.keys():

                            default_value, default_condition = self._default_values[k]

                            if default_condition(dict_row[k]):

                                if callable(default_value):
                                    dict_row[k] = default_value()
                                else:
                                    dict_row[k] = str(default_value)

                                update_[0] = True

                    # Map the entry (dict_row) by the indexed field
                    new_index = self.construct_key(dict_row)

                    self._indexed_field_map[new_index] = dict_row

                    yield dict_row

        self._entries = tuple(load_entries(update))

        if update[0]:
            self.save()

        return self

    def apply_default_values(self):

        update = False

        for entry in self._indexed_field_map.values():
            for default_k, default_v in self._default_values.items():
                if entry[default_k].strip() == '':
                    update = True
                    if isinstance(default_v, str):
                        entry[default_k] = default_v
                    elif callable(default_v):
                        entry[default_k] = default_v()

        if update:
            self.save()

        return self

    def __str__(self):
        return str(self._entries)


def multi_key_demo():
    import rskeyring
    import sys
    import json
    import os

    def store_secret(key, secret):
        rskeyring.set_password("test", key, secret)
        return True

    def get_secret(key):
        return rskeyring.get_password("test", key)

    with open(sys.argv[1], 'w') as fs:
        fs.write('username,company,api-key,secret,comments\n')
        fs.write('test_user,Kola,aabbcc,paswd, A test thingy\n')
        fs.write('test_user2,Kola,12345,zzzzz, A test thingy2\n')
        fs.write('test_user,RED HAT,qwe,ghhh, A test thingy3\n')

    clients_csv = CsvManager(
        sys.argv[1],
        key_fields=('username', 'company'),
        secret_fields=('api-key', 'secret'),
        store_secret=store_secret,
        get_secret=get_secret,
    )

    print(clients_csv.json_string())
    print(clients_csv.json_string(('test_user', 'RED HAT')))

    print(clients_csv.get_titles())

    print(clients_csv.get_entry(('test_user2', 'Kola')))  # Extracted from indexed field. In this case, 'username'

    print(clients_csv.get_secret(('test_user', 'RED HAT'), 'api-key'))

    for entry in clients_csv.get_entries():
        entry_json = json.dumps(entry, indent=4)
        print(entry_json)

    for exposed_entry in clients_csv.exposed_entries():
        exposed_entry_json = json.dumps(exposed_entry, indent=4)
        print(exposed_entry_json)

    os.remove(sys.argv[1])


def single_key_demo():
    import rskeyring
    import sys
    import json
    import os

    def store_secret(key, secret):
        rskeyring.set_password("test", key, secret)
        return True

    def get_secret(key):
        return rskeyring.get_password("test", key)

    with open(sys.argv[1], 'w') as fs:
        fs.write('username,company,api-key,secret,comments\n')
        fs.write('test_user,Kola,aabbcc,paswd, A test thingy\n')
        fs.write('test_user2,Kola,12345,zzzzz, A test thingy2\n')
        fs.write('test_user3,RED HAT,qwe,ghhh, A test thingy3\n')

    clients_csv = CsvManager(
        sys.argv[1],
        key_fields='username',
        secret_fields=('api-key', 'secret'),
        store_secret=store_secret,
        get_secret=get_secret,
    )

    print(clients_csv.json_string())
    print(clients_csv.json_string('test_user'))

    print(clients_csv.get_titles())

    print(clients_csv.get_entry('test_user2'))  # Extracted from indexed field. In this case, 'username'

    print(clients_csv.get_secret('test_user', 'api-key'))

    for entry in clients_csv.get_entries():
        entry_json = json.dumps(entry, indent=4)
        print(entry_json)

    for exposed_entry in clients_csv.exposed_entries():
        exposed_entry_json = json.dumps(exposed_entry, indent=4)
        print(exposed_entry_json)

    os.remove(sys.argv[1])


if __name__ == '__main__':
    multi_key_demo()
    # single_key_demo()
