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

from typing import Tuple

from siemkit.api.arcsight.esm import ArcSightUri


class AddEntries(ArcSightUri):

    def args(self, variables, resource_id='', columns=None, entries=None) -> Tuple[str, dict]:

        if columns is None:
            columns = []  # Relevant columns in proper order
        if isinstance(columns, str):
            columns = [columns]
        else:
            columns = list(columns)

        if entries is None:
            entries = []  # Entries of dict with relevant columns
        elif isinstance(entries, dict):
            entries = [entries]
        else:
            entries = list(entries)

        entry_columns = []
        entry_list = []

        for entry in entries:
            for column in columns:
                entry_columns.append(entry[column])

            entry_list.append(
                {
                    'entry': entry_columns
                }
            )

            entry_columns.clear()

        return (
            '/www/manager-service/rest/ActiveListService/addEntries',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    "act.addEntries": {
                        "act.authToken": variables.get('token', ''),
                        "act.resourceId": resource_id,
                        "act.entryList": {
                            "columns": columns,
                            "entryList": entry_list
                        }
                    }
                }
            }
        )


class ClearEntries(ArcSightUri):

    def args(self, variables, resource_id='') -> Tuple[str, dict]:

        return (
            '/www/manager-service/rest/ActiveListService/clearEntries',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    "act.clearEntries": {
                        "act.authToken": variables.get('token', ''),
                        "act.resourceId": resource_id
                    }
                }
            }
        )


class DeleteEntries(ArcSightUri):

    def args(self, variables, resource_id='', columns=None, entries=None) -> Tuple[str, dict]:

        if columns is None:
            columns = []  # Relevant columns in proper order
        if isinstance(columns, str):
            columns = [columns]
        else:
            columns = list(columns)

        if entries is None:
            entries = []  # Entries of dict with relevant columns
        elif isinstance(entries, dict):
            entries = [entries]
        else:
            entries = list(entries)

        entry_columns = []
        entry_list = []

        for entry in entries:
            for column in columns:
                entry_columns.append(entry[column])

            entry_list.append(
                {
                    'entry': entry_columns
                }
            )

            entry_columns.clear()

        return (
            '/www/manager-service/rest/ActiveListService/deleteEntries',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    "act.deleteEntries": {
                        "act.authToken": variables.get('token', ''),
                        "act.resourceId": resource_id,
                        "act.entryList": {
                            "columns": columns,
                            "entryList": entry_list
                        }
                    }
                }
            }
        )


class GetEntries(ArcSightUri):

    def args(self, variables, resource_id='') -> Tuple[str, dict]:

        return (
            '/www/manager-service/rest/ActiveListService/getEntries',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    "act.getEntries": {
                        "act.authToken": variables.get('token', ''),
                        "act.resourceId": resource_id
                    }
                }
            }
        )


class FindAllIds(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:
        return (
            '/www/manager-service/rest/ActiveListService/findAllIds',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                    {
                        "act.findAllIds": {
                            "act.authToken": variables.get('token', '')
                        }
                    }
                }
            }
        )
