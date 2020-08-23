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
from siemkit.api.arcsight.esm import ArcSightUriEnum


def init_columns_entries(variables):
    """
    Making sure we have `columns` & `entries` to return, without effecting the original objects.
    """

    columns = variables.get('columns')
    if columns is None:
        columns = []  # Relevant columns in proper order
    if isinstance(columns, str):
        columns = [columns]
    else:
        columns = list(columns)

    entries = variables.get('entries')
    if entries is None:
        entries = []  # Entries of dict with relevant columns
    elif isinstance(entries, dict):
        entries = [entries]
    else:
        entries = list(entries)

    return columns, entries


class AddEntries(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:

        columns, entries = init_columns_entries(variables)

        entry_columns = []
        entry_list = []

        # Build JSON
        for entry in entries:
            for column in columns:
                entry_columns.append(entry[column])

            entry_list.append(
                {
                    'entry': list(entry_columns)
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
                        "act.resourceId": variables.get('resource_id', ''),
                        "act.entryList": {
                            "columns": columns,
                            "entryList": entry_list
                        }
                    }
                }
            }
        )


class ClearEntries(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:

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
                        "act.resourceId": variables.get('resource_id', '')
                    }
                }
            }
        )


class DeleteEntries(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:

        columns, entries = init_columns_entries(variables)

        entry_columns = []
        entry_list = []

        # Build JSON
        for entry in entries:
            for column in columns:
                entry_columns.append(entry[column])

            entry_list.append(
                {
                    'entry': list(entry_columns)
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
                        "act.resourceId": variables.get('resource_id', ''),
                        "act.entryList": {
                            "columns": columns,
                            "entryList": entry_list
                        }
                    }
                }
            }
        )


class GetEntries(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:

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
                        "act.resourceId": variables.get('resource_id', '')
                    }
                }
            }
        )


class FindByUuid(ArcSightUri):

    def args(self, variables) -> Tuple[str, dict]:
        return (
            '/www/manager-service/rest/ActiveListService/findByUUID',
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                'method': 'POST',
                'json': {
                        "act.findByUUID": {
                            "act.authToken": variables.get('token', ''),
                            "act.id": variables.get("uuid", '')
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
                        "act.findAllIds": {
                            "act.authToken": variables.get('token', '')
                        }
                }
            }
        )


class ActiveListApiEnum(ArcSightUriEnum):
    GET_ENTRIES = GetEntries()
    ADD_ENTRIES = AddEntries()
    DELETE_ENTRIES = DeleteEntries()
    CLEAR_ENTRIES = ClearEntries()
    FIND_ALL_IDS = FindAllIds()
    FIND_BY_UUID = FindByUuid()
