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

import csv


class CSVConf:

    def __init__(
            self,
            csv_file,
            indexed_field,
            secret_fields,
            newline='',
            encoding='utf-8',
            errors='ignore',
            store_secret=None,
            get_secret=None
    ):
        """

        :param csv_file: A path to the configurations CSV file
        :param indexed_field: An indexed field to group data by. e.g. username, id, email, etc.
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
        """

        if indexed_field in secret_fields:
            raise Exception(f"Secret field '{indexed_field}' cannot be indexed field.")

        self._csv_file = csv_file
        self._indexed_field = indexed_field
        self._secret_fields = secret_fields
        self._newline = newline
        self._encoding = encoding
        self._errors = errors
        self._store_secret = store_secret
        self._get_secret = get_secret

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
        return self._indexed_field_map[index]

    def exposed_entries(self):
        """
        Generates an exposed entry at a time, restoring its secret fields.
        :return:
        """

        for entry in self._entries:
            exposed_entry = dict(entry)

            for secret_field in self._secret_fields:
                exposed_entry[secret_field] = self.get_secret(entry[self._indexed_field], secret_field)

            yield exposed_entry

    def get_entries(self):
        return tuple(self._entries)

    def store_secret(self, entry, secret_key):

        if callable(self._store_secret):
            key = f"{entry[self._indexed_field]}.{secret_key}"
            if self._store_secret(key, entry[secret_key]):
                entry[secret_key] = 'stored'

        return self

    def get_secret(self, entry_index, secret_key):
        if callable(self._get_secret):
            key = f"{entry_index}.{secret_key}"
            return self._get_secret(key)

    def get_indexed_field(self):
        return self._indexed_field

    def get_secret_fields(self):
        return self._secret_fields

    def save(self):
        """
        Commit changes to CSV file.
        :return: self
        """

        with open(self._csv_file, 'w', encoding=self._encoding, errors=self._errors, newline=self._newline) as fs:
            fs.seek(0)
            writer = csv.DictWriter(fs, fieldnames=self._titles)
            writer.writeheader()
            for entry in self._entries:
                del entry['_line']
                writer.writerow(entry)

        return self

    def load(self):
        """
        Load or Reload CSV file.
        :return: self
        """

        update = [False]

        def load_entries(update_):

            with open(self._csv_file, newline=self._newline, encoding=self._encoding, errors=self._errors) as fs:

                self._titles = tuple(next(csv.reader(fs)))

                fs.seek(0)

                csv_dict_ = csv.DictReader(fs)

                for i, row in enumerate(csv_dict_):

                    dict_row = dict(row)
                    dict_row['_line'] = i + 1

                    for k in dict_row.keys():
                        if k in self._secret_fields:
                            if str(dict_row[k]).lower().strip() != 'stored':
                                if callable(self._store_secret):
                                    self.store_secret(dict_row, k)
                                    update_[0] = True

                    self._indexed_field_map[dict_row[self._indexed_field]] = dict_row

                    yield dict_row

        self._entries = tuple(load_entries(update))

        if update[0]:
            self.save()

        return self

    def __str__(self):
        return str(self._entries)


def demo():
    import rskeyring
    import sys
    import json

    def store_secret(key, secret):
        rskeyring.set_password("test", key, secret)
        return True

    def get_secret(key):
        return rskeyring.get_password("test", key)

    clients_csv = CSVConf(
        sys.argv[1],
        indexed_field='username',
        secret_fields=('api-key', 'secret'),
        store_secret=store_secret,
        get_secret=get_secret
    )
    print(clients_csv.get_entry('nice'))  # Extracted from indexed field. In this case, 'username'

    print(clients_csv.get_titles())

    print(clients_csv.get_secret('nice', 'api-key'))

    for entry in clients_csv.get_entries():
        entry_json = json.dumps(entry, indent=4)
        print(entry_json)

    for exposed_entry in clients_csv.exposed_entries():
        exposed_entry_json = json.dumps(exposed_entry, indent=4)
        print(exposed_entry_json)


if __name__ == '__main__':
    demo()
